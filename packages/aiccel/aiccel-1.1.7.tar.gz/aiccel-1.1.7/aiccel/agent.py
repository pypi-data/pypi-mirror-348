import json
import re
import asyncio
import traceback
import zlib
import requests
from typing import List, Dict, Any, Optional, Tuple, Union, Callable
from datetime import datetime
import orjson
from cachetools import TTLCache
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import aiohttp

from .tools import Tool, ToolRegistry
from .providers import LLMProvider
from .logger import AILogger

# Global tracing configuration
_tracing_config = {
    "api_key": None,
    "backend_url": "http://localhost:8000",
    "enabled": False
}

def init_tracing(api_key: str, backend_url: str = "http://localhost:8000"):
    """Initialize tracing for aiccl, similar to LangTrace SDK"""
    global _tracing_config
    _tracing_config["api_key"] = api_key
    _tracing_config["backend_url"] = backend_url
    _tracing_config["enabled"] = True
    
    # Validate API key
    try:
        response = requests.get(
            f"{backend_url}/api/validate/{api_key}",
            timeout=5
        )
        response.raise_for_status()
        data = response.json()
        if not data.get("valid"):
            raise ValueError("Invalid API key")
    except Exception as e:
        raise ValueError(f"Failed to validate API key: {str(e)}")

class ConversationMemory:
    """Manages conversational memory for the agent"""
    def __init__(self, memory_type: str = "buffer", max_turns: int = 10, max_tokens: int = 1000, llm_provider: Optional[LLMProvider] = None):
        self.memory_type = memory_type
        self.max_turns = max_turns
        self.max_tokens = max_tokens
        self.llm_provider = llm_provider
        self.history = []
        self._token_cache = 0
        self._validate_config()

    def _validate_config(self):
        if self.memory_type not in ["buffer", "window", "summary"]:
            raise ValueError("memory_type must be 'buffer', 'window', or 'summary'")
        if self.memory_type == "summary" and not self.llm_provider:
            raise ValueError("summary memory requires an llm_provider")

    def add_turn(self, query: str, response: str, tool_used: Optional[str] = None, tool_output: Optional[str] = None):
        turn = {
            "query": zlib.compress(query[:1000].encode('utf-8')).hex(),
            "response": zlib.compress(response[:1000].encode('utf-8')).hex(),
            "tool_used": tool_used,
            "tool_output": zlib.compress(tool_output[:1000].encode('utf-8')).hex() if tool_output else None,
            "timestamp": datetime.now().isoformat()
        }
        self.history.append(turn)
        self._token_cache += (len(query) + len(response) + (len(tool_output) if tool_output else 0)) // 4
        self._manage_memory()

    def _manage_memory(self):
        while (len(self.history) > self.max_turns or self._token_cache > self.max_tokens) and self.history:
            removed = self.history.pop(0)
            self._token_cache -= (len(zlib.decompress(bytes.fromhex(removed["query"])).decode('utf-8')) +
                                  len(zlib.decompress(bytes.fromhex(removed["response"])).decode('utf-8')) +
                                  (len(zlib.decompress(bytes.fromhex(removed["tool_output"])).decode('utf-8')) if removed["tool_output"] else 0)) // 4
        if self.memory_type == "summary" and len(self.history) > self.max_turns // 2:
            self._summarize_history()

    def _approximate_tokens(self) -> int:
        return self._token_cache

    def _summarize_history(self):
        if len(self.history) <= 1 or not self.llm_provider:
            return

        to_summarize = self.history[:-1]
        summary_prompt = (
            "Summarize the following conversation history into a concise summary (max 200 words):\n\n"
        )
        for turn in to_summarize:
            query = zlib.decompress(bytes.fromhex(turn["query"])).decode('utf-8')
            response = zlib.decompress(bytes.fromhex(turn["response"])).decode('utf-8')
            summary_prompt += f"User: {query}\nAssistant: {response}\n"
            if turn["tool_output"]:
                tool_output = zlib.decompress(bytes.fromhex(turn["tool_output"])).decode('utf-8')
                summary_prompt += f"Tool Output: {tool_output}\n"
        
        summary = self.llm_provider.generate(summary_prompt)
        
        self.history = [{
            "query": zlib.compress("Conversation summary".encode('utf-8')).hex(),
            "response": zlib.compress(summary.encode('utf-8')).hex(),
            "tool_used": None,
            "tool_output": None,
            "timestamp": datetime.now().isoformat()
        }] + self.history[-1:]

    def get_context(self, max_context_turns: Optional[int] = None) -> str:
        if not self.history:
            return ""

        context = "Conversation History:\n"
        turns = self.history[-max_context_turns:] if max_context_turns else self.history
        
        for turn in turns:
            query = zlib.decompress(bytes.fromhex(turn["query"])).decode('utf-8')
            response = zlib.decompress(bytes.fromhex(turn["response"])).decode('utf-8')
            context += f"User: {query}\nAssistant: {response}\n"
            if turn["tool_used"] and turn["tool_output"]:
                tool_output = zlib.decompress(bytes.fromhex(turn["tool_output"])).decode('utf-8')
                context += f"Tool Used: {turn['tool_used']}\nTool Output: {tool_output}\n"
            context += "\n"
        
        token_count = len(context) // 4
        if token_count > 2000:
            context = context[-8000:]  # Roughly 2000 tokens
        return context.strip()

    def clear(self):
        self.history = []
        self._token_cache = 0

    def get_history(self) -> List[Dict[str, Any]]:
        return [
            {
                "query": zlib.decompress(bytes.fromhex(turn["query"])).decode('utf-8'),
                "response": zlib.decompress(bytes.fromhex(turn["response"])).decode('utf-8'),
                "tool_used": turn["tool_used"],
                "tool_output": zlib.decompress(bytes.fromhex(turn["tool_output"])).decode('utf-8') if turn["tool_output"] else None,
                "timestamp": turn["timestamp"]
            }
            for turn in self.history
        ]

class Agent:
    _tool_prompt_cache = TTLCache(maxsize=100, ttl=3600)  # Cache for tool prompt parts

    def __init__(self,
                 provider: LLMProvider,
                 tools: Optional[Union[List[Tool], ToolRegistry]] = None,
                 verbose: bool = False,
                 name: Optional[str] = None,
                 log_file: Optional[str] = None,
                 instructions: Optional[str] = None,
                 description: Optional[str] = None,
                 memory_type: str = "buffer",
                 max_memory_turns: int = 10,
                 max_memory_tokens: int = 1000,
                 strict_tool_usage: bool = False,
                 fallback_providers: Optional[List[LLMProvider]] = None):
        self.provider = provider
        self.name = name or "CollectorAgent"
        self.description = description or "General-purpose AI agent"
        self.verbose = verbose
        self.logger = AILogger(self.name, verbose, log_file, structured_logging=True)
        self.instructions = instructions or "You are a helpful AI assistant. Provide accurate and concise answers."

        self.tool_registry = ToolRegistry(llm_provider=provider)
        self.tools = tools if tools is not None else []
        if isinstance(tools, list):
            self.tool_registry.register_all(tools)
        elif isinstance(tools, ToolRegistry):
            self.tool_registry = tools
            self.tool_registry.llm_provider = provider

        self.strict_tool_usage = strict_tool_usage
        self.tool_cache = TTLCache(maxsize=1000, ttl=3600)  # Cache for tool outputs
        has_any_tools = bool(self.tool_registry.get_all())

        if self.strict_tool_usage and has_any_tools:
            strict_addon = (
                " You MUST use the available tools to answer queries. "
                "If the tools cannot provide an answer, or if the query is outside the scope of the tools, "
                "you MUST state that you cannot answer the query using the provided tools. "
                "Do NOT use your general knowledge in such cases."
            )
            if "MUST use the available tools" not in self.instructions and \
               "MUST use the" not in self.instructions and \
               "can ONLY respond based on information in the documents" not in self.instructions:
                self.instructions += strict_addon
            self.logger.log(f"Agent '{self.name}' configured with strict_tool_usage=True. Effective instructions: '{self.instructions}'")
        elif self.strict_tool_usage and not has_any_tools:
            self.logger.log(f"Agent '{self.name}' has strict_tool_usage=True but no tools are registered. This may lead to unexpected 'cannot answer' responses.")

        self.thinking_enabled = False
        self.fallback_providers = fallback_providers or []

        self.memory = ConversationMemory(
            memory_type=memory_type,
            max_turns=max_memory_turns,
            max_tokens=max_memory_tokens,
            llm_provider=provider
        )

        if _tracing_config["enabled"]:
            self.logger.log(f"Tracing enabled with API key: {_tracing_config['api_key'][:4]}... to {_tracing_config['backend_url']}")

        if self.verbose:
            self.logger.log(f"Agent {self.name} initialized with {len(self.tool_registry.get_all())} tools. Description: {self.description}. Strict tool usage: {self.strict_tool_usage}")

    @classmethod
    def from_provider(cls, provider: LLMProvider, name: Optional[str] = None, verbose: bool = False, 
                     log_file: Optional[str] = None, instructions: Optional[str] = None,
                     description: Optional[str] = None,
                     memory_type: str = "buffer", max_memory_turns: int = 10, max_memory_tokens: int = 1000,
                     fallback_providers: Optional[List[LLMProvider]] = None):
        return cls(
            provider=provider, 
            tools=None, 
            verbose=verbose, 
            name=name, 
            log_file=log_file, 
            instructions=instructions,
            description=description,
            memory_type=memory_type,
            max_memory_turns=max_memory_turns,
            max_memory_tokens=max_memory_tokens,
            fallback_providers=fallback_providers
        )
    
    def log(self, message: str, exc_info: Optional[Exception] = None) -> None:
        self.logger.log(message, exc_info=exc_info)
    
    def enable_thinking(self, enabled: bool = True) -> 'Agent':
        self.thinking_enabled = enabled
        if enabled and self.verbose:
            self.logger.log("Thinking mode enabled")
        return self
    
    def set_verbose(self, verbose: bool = True) -> 'Agent':
        self.verbose = verbose
        self.logger.verbose = verbose
        return self
    
    def set_instructions(self, instructions: str) -> 'Agent':
        self.instructions = instructions
        if self.verbose:
            self.logger.log(f"Updated instructions: {instructions[:50]}...")
        return self
    
    def set_description(self, description: str) -> 'Agent':
        self.description = description
        if self.verbose:
            self.logger.log(f"Updated description: {description[:50]}...")
        return self
    
    def with_tool(self, tool: Tool) -> 'Agent':
        self.tool_registry.register(tool)
        self.tools.append(tool)
        if self.verbose:
            self.logger.log(f"Added tool: {tool.name}")
        return self
    
    def with_tools(self, tools: List[Tool]) -> 'Agent':
        self.tool_registry.register_all(tools)
        self.tools.extend(tools)
        if self.verbose:
            self.logger.log(f"Added {len(tools)} tools")
        return self
    
    def sync_tools_to_registry(self) -> 'Agent':
        self.tool_registry = ToolRegistry(llm_provider=self.provider)
        if self.tools:
            self.tool_registry.register_all(self.tools)
        if self.verbose:
            self.logger.log(f"Synchronized tool_registry with {len(self.tool_registry.get_all())} tools")
        return self
    
    def clear_memory(self) -> 'Agent':
        self.memory.clear()
        self.logger.log("Conversation memory cleared")
        return self
    
    def set_memory_type(self, memory_type: str) -> 'Agent':
        self.memory.memory_type = memory_type
        self.memory._validate_config()
        self.logger.log(f"Memory type set to: {memory_type}")
        return self
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=0.5, min=2, max=8),
        retry=retry_if_exception_type((Exception,)),
        reraise=True
    )
    def call(self, prompt: str, **kwargs) -> str:
        trace_id = self.logger.trace_start("simple_call", {"prompt": prompt[:100] + "..." if len(prompt) > 100 else prompt})
        
        self.logger.log(f"Making simple call: {prompt[:50]}...")
        try:
            response = self.provider.generate(prompt, **kwargs)
            self.logger.trace_step(trace_id, "response_received", 
                                  {"response": response[:100] + "..." if len(response) > 100 else response})
            self.logger.trace_end(trace_id, {"response": response})
            return response
        except Exception as e:
            self.logger.trace_error(trace_id, e, "Failed to generate response")
            for fallback in self.fallback_providers:
                try:
                    self.logger.log(f"Falling back to provider: {type(fallback).__name__}")
                    response = fallback.generate(prompt, **kwargs)
                    self.logger.trace_step(trace_id, "fallback_response_received", 
                                          {"response": response[:100] + "..." if len(response) > 100 else response})
                    self.logger.trace_end(trace_id, {"response": response})
                    return response
                except Exception as fb_e:
                    self.logger.trace_error(trace_id, fb_e, f"Fallback provider {type(fallback).__name__} failed")
            raise Exception(f"All providers failed: {str(e)}")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=0.5, min=2, max=8),
        retry=retry_if_exception_type((Exception,)),
        reraise=True
    )
    async def call_async(self, prompt: str, **kwargs) -> str:
        trace_id = self.logger.trace_start("simple_call_async", 
                                          {"prompt": prompt[:100] + "..." if len(prompt) > 100 else prompt})
        
        self.logger.log(f"Making async simple call: {prompt[:50]}...")
        try:
            response = await self.provider.generate_async(prompt, **kwargs)
            self.logger.trace_step(trace_id, "response_received", 
                                  {"response": response[:100] + "..." if len(response) > 100 else response})
            self.logger.trace_end(trace_id, {"response": response})
            return response
        except Exception as e:
            self.logger.trace_error(trace_id, e, "Failed to generate async response")
            for fallback in self.fallback_providers:
                try:
                    self.logger.log(f"Falling back to provider: {type(fallback).__name__}")
                    response = await fallback.generate_async(prompt, **kwargs)
                    self.logger.trace_step(trace_id, "fallback_response_received", 
                                          {"response": response[:100] + "..." if len(response) > 100 else response})
                    self.logger.trace_end(trace_id, {"response": response})
                    return response
                except Exception as fb_e:
                    self.logger.trace_error(trace_id, fb_e, f"Fallback provider {type(fallback).__name__} failed")
            raise Exception(f"All providers failed: {str(e)}")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=0.5, min=2, max=8),
        retry=retry_if_exception_type((Exception,)),
        reraise=True
    )
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        trace_id = self.logger.trace_start("chat_call", {"messages_count": len(messages)})
        
        self.logger.log(f"Making chat call with {len(messages)} messages")
        try:
            response = self.provider.chat(messages, **kwargs)
            self.logger.trace_step(trace_id, "response_received", 
                                  {"response": response[:100] + "..." if len(response) > 100 else response})
            self.logger.trace_end(trace_id, {"response": response})
            return response
        except Exception as e:
            self.logger.trace_error(trace_id, e, "Failed to process chat")
            for fallback in self.fallback_providers:
                try:
                    self.logger.log(f"Falling back to provider: {type(fallback).__name__}")
                    response = fallback.chat(messages, **kwargs)
                    self.logger.trace_step(trace_id, "fallback_response_received", 
                                          {"response": response[:100] + "..." if len(response) > 100 else response})
                    self.logger.trace_end(trace_id, {"response": response})
                    return response
                except Exception as fb_e:
                    self.logger.trace_error(trace_id, fb_e, f"Fallback provider {type(fallback).__name__} failed")
            raise Exception(f"All providers failed: {str(e)}")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=0.5, min=2, max=8),
        retry=retry_if_exception_type((Exception,)),
        reraise=True
    )
    async def chat_async(self, messages: List[Dict[str, str]], **kwargs) -> str:
        trace_id = self.logger.trace_start("chat_call_async", {"messages_count": len(messages)})
        
        self.logger.log(f"Making async chat call with {len(messages)} messages")
        try:
            response = await self.provider.chat_async(messages, **kwargs)
            self.logger.trace_step(trace_id, "response_received", 
                                  {"response": response[:100] + "..." if len(response) > 100 else response})
            self.logger.trace_end(trace_id, {"response": response})
            return response
        except Exception as e:
            self.logger.trace_error(trace_id, e, "Failed to process async chat")
            for fallback in self.fallback_providers:
                try:
                    self.logger.log(f"Falling back to provider: {type(fallback).__name__}")
                    response = await fallback.chat_async(messages, **kwargs)
                    self.logger.trace_step(trace_id, "fallback_response_received", 
                                          {"response": response[:100] + "..." if len(response) > 100 else response})
                    self.logger.trace_end(trace_id, {"response": response})
                    return response
                except Exception as fb_e:
                    self.logger.trace_error(trace_id, fb_e, f"Fallback provider {type(fallback).__name__} failed")
            raise Exception(f"All providers failed: {str(e)}")
    
    def _find_relevant_tools(self, query: str) -> List[Tool]:
        return self.tool_registry.find_relevant_tools(query)
    
    def _build_static_prompt_parts(self) -> Dict[str, str]:
        has_any_tools = bool(self.tool_registry.get_all())
        tool_key = tuple(sorted(t.name for t in self.tool_registry.get_all()))
        if tool_key not in self._tool_prompt_cache:
            tool_descriptions = "\n".join(
                f"- {tool.name}: {tool.description}\n  Example usage: [TOOL]{orjson.dumps({'name': tool.name, 'args': tool.example_usages[0]['args'] if tool.example_usages else {'param': 'value'}}).decode('utf-8')}[/TOOL]"
                for tool in self.tool_registry.get_all()
            )
            self._tool_prompt_cache[tool_key] = tool_descriptions
        else:
            tool_descriptions = self._tool_prompt_cache[tool_key]
        return {
            "base": f"Instructions: {self.instructions}\n\n",
            "tools": (
                f"Available tools:\n{tool_descriptions}\n\n"
                "Tool usage decision process:\n"
                "1. Analyze the query to determine if any of the available tools can help answer it.\n"
                f"2. If multiple tools are relevant, include ALL necessary tool calls in your response, each using the EXACT format:\n"
                f"   [TOOL]{{\"name\":\"tool_name\",\"args\":{{\"parameter_name\":\"parameter_value\"}}}}[/TOOL]\n"
                f"3. If only one tool is needed, include a single tool call in the same format.\n"
                f"4. If no tool is needed, or you can answer directly with high confidence, "
                f"provide a direct response without [TOOL] tags.\n"
                "\nExamples of tool usage:\n"
                "- For a query like 'what's the weather in Trivandrum and in Kochi?', you might include:\n"
                "  [TOOL]{\"name\":\"get_weather\",\"args\":{\"location\":\"Trivandrum\"}}[/TOOL]\n"
                "  [TOOL]{\"name\":\"get_weather\",\"args\":{\"location\":\"Kochi\"}}[/TOOL]\n"
                "- For a query like 'tell me about Aromal TR and what's the weather in Trivandrum', you might include:\n"
                "  [TOOL]{\"name\":\"search\",\"args\":{\"query\":\"Aromal TR\"}}[/TOOL]\n"
                "  [TOOL]{\"name\":\"get_weather\",\"args\":{\"location\":\"Trivandrum\"}}[/TOOL]\n"
                "Make sure to use the appropriate tools for each part of the query."
                if not self.strict_tool_usage else
                f"2. You MUST select and use at least one tool to answer the query, including ALL relevant tools if multiple apply. "
                f"Format each tool call using the EXACT format:\n"
                f"   [TOOL]{{\"name\":\"tool_name\",\"args\":{{\"parameter_name\":\"parameter_value\"}}}}[/TOOL]\n"
                f"3. If no tool is appropriate, or if a tool attempt fails, "
                f"output only:\n"
                f"   [NO_TOOL]No appropriate tool available or tool failed. Cannot answer.[/NO_TOOL]\n"
                f"4. Do NOT generate any response content outside of [TOOL] or [NO_TOOL] tags.\n"
                "\nExamples of tool usage:\n"
                "- For a query like 'what's the weather in Trivandrum and in Kochi?', you MUST include:\n"
                "  [TOOL]{\"name\":\"get_weather\",\"args\":{\"location\":\"Trivandrum\"}}[/TOOL]\n"
                "  [TOOL]{\"name\":\"get_weather\",\"args\":{\"location\":\"Kochi\"}}[/TOOL]\n"
                "- For a query like 'tell me about Aromal TR and what's the weather in Trivandrum', you MUST include:\n"
                "  [TOOL]{\"name\":\"search\",\"args\":{\"query\":\"Aromal TR\"}}[/TOOL]\n"
                "  [TOOL]{\"name\":\"get_weather\",\"args\":{\"location\":\"Trivandrum\"}}[/TOOL]\n"
                "Ensure all parts of the query are addressed using the appropriate tools."
            ) if has_any_tools else "",
            "no_tools": (
                "No tools are available. Answer the query directly based on your knowledge and the main instructions.\n"
                if not self.strict_tool_usage else
                "No tools are available. In strict tool usage mode, I cannot answer the query without tools.\n"
                "Output: [NO_TOOL]No tools available. Cannot answer.[/NO_TOOL]"
            )
        }

    def _build_enhanced_prompt(self, query: str, relevant_tools: List[Tool]) -> str:
        static_parts = self._build_static_prompt_parts()
        parts = [static_parts["base"]]
        
        context = self.memory.get_context(max_context_turns=5)
        if context:
            parts.append(f"{context}\n\n")

        parts.append(f"Current Query: {query[:1000]}\n\n")
        parts.append("Follow these steps to respond:\n\n")
        parts.append(static_parts["tools"])

        if relevant_tools:
            parts.append(f"The following tools seem particularly relevant for this query: {', '.join(t.name for t in relevant_tools)}\n")
            if self.strict_tool_usage:
                parts.append("You should strongly prioritize using these tools if applicable, including all relevant tools for multi-part queries.\n")
        elif self.strict_tool_usage and self.tool_registry.get_all():
            parts.append(
                "Even if no specific tools were pre-identified as relevant, "
                "you MUST still attempt to select and use all appropriate tools if the query can potentially be addressed by any of the available tools.\n"
                "If no tool applies, output [NO_TOOL] as specified above.\n"
            )
        
        parts.append(static_parts["no_tools"])
        parts.append("\nProvide your response below, adhering strictly to the tool usage instructions if tools are available.")
        return "".join(parts)
    
    def _parse_tool_usage(self, response: str, original_query: str = "") -> List[Tuple[Optional[str], Optional[Dict[str, Any]]]]:
        # Modified to parse multiple [TOOL] tags
        tool_calls = []
        no_tool_pattern = r'\[NO_TOOL\](.*?)\[/NO_TOOL\]'
        no_tool_match = re.search(no_tool_pattern, response, re.DOTALL)
        if no_tool_match and self.strict_tool_usage:
            self.logger.log("Parsed [NO_TOOL] tag, indicating no appropriate tool.")
            return []

        tool_pattern = r'\[TOOL\](.*?)\[/TOOL\]'
        matches = re.findall(tool_pattern, response, re.DOTALL)
        
        for match in matches:
            try:
                tool_json = match.strip()
                tool_data = orjson.loads(tool_json)
                tool_name = tool_data.get("name")
                tool_args = tool_data.get("args", {})
                if tool_name == "pdf_rag" and not tool_args.get("query") and original_query:
                    tool_args["query"] = original_query
                tool_calls.append((tool_name, tool_args))
            except Exception as e:
                self.logger.trace_error(0, e, "Failed to parse tool JSON")
                continue

        if not matches:
            # Try alternate patterns for robustness
            alt_patterns = [
                r'```json\n\s*{\s*"name":\s*"([^"]+)",\s*"args":\s*{(.*?)}\s*}\s*```',
                r'Tool:\s*([a-z_]+).*?Args:.*?(\{.*?\}|\w+:\s*[^,\n]+)',
                r'(\w+)\s*\(\s*(?:query|location):\s*"([^"]+)"\s*\)'
            ]
            
            for pattern in alt_patterns:
                alt_matches = re.findall(pattern, response, re.DOTALL)
                for alt_match in alt_matches:
                    try:
                        if '{' in alt_match[0] or '{' in alt_match[1]:
                            tool_json = re.sub(r'Tool:|Args:', '', alt_match[0] + alt_match[1])
                            tool_data = orjson.loads(tool_json)
                            tool_name = tool_data.get("name")
                            tool_args = tool_data.get("args", {})
                            if tool_name == "pdf_rag" and not tool_args.get("query") and original_query:
                                tool_args["query"] = original_query
                            tool_calls.append((tool_name, tool_args))
                        else:
                            tool_name = alt_match[0]
                            arg_text = alt_match[1]
                            tool = self.tool_registry.get(tool_name)
                            if tool:
                                tool_spec = tool.to_dict()
                                if "parameters" in tool_spec and "properties" in tool_spec["parameters"]:
                                    first_param = next(iter(tool_spec["parameters"]["properties"]))
                                    args = {first_param: arg_text.strip()}
                                    if tool_name == "pdf_rag" and first_param == "query" and not args.get("query") and original_query:
                                        args["query"] = original_query
                                    tool_calls.append((tool_name, args))
                            if tool_name == "search":
                                tool_calls.append((tool_name, {"query": arg_text.strip()}))
                            elif tool_name == "get_weather":
                                tool_calls.append((tool_name, {"location": arg_text.strip()}))
                    except Exception as e:
                        self.logger.trace_error(0, e, "Failed to parse alternate tool pattern")
                        continue
        
        if self.tool_registry.get_all() and not tool_calls:
            check_prompt = (
                f"Query: {original_query}\n"
                f"Response: {response}\n\n"
                f"Available tools: {', '.join([t.name for t in self.tool_registry.get_all()])}\n\n"
                "Does this response imply that multiple tools should have been used? If so, return a list of tool calls in JSON format:\n"
                "```json\n[{\"name\": \"tool_name\", \"args\": {\"query\": \"value\"}}, ...]\n```"
                "If no tools are implied, return an empty list:\n"
                "```json\n[]\n```"
            )
            try:
                check_response = self.call(check_prompt)
                tool_data_list = orjson.loads(check_response.strip())
                for tool_data in tool_data_list:
                    if tool_data and "name" in tool_data:
                        tool_name = tool_data["name"]
                        tool_args = tool_data.get("args", {})
                        if tool_name == "pdf_rag" and not tool_args.get("query") and original_query:
                            tool_args["query"] = original_query
                        tool_calls.append((tool_name, tool_args))
            except Exception as e:
                self.logger.trace_error(0, e, "Failed to check implied tool usage")
        
        return tool_calls
    
    def _create_direct_tool_prompt(self, query: str, relevant_tools: List[Tool]) -> str:
        tool_descriptions = "\n".join(
            [f"- {tool.name}: {tool.description}\n  Example: [TOOL]{orjson.dumps({'name': tool.name, 'args': tool.example_usages[0]['args'] if tool.example_usages else {'query': query}}).decode('utf-8')}[/TOOL]" 
             for tool in relevant_tools]
        )
        direct_tool_prompt = (
            f"Instructions: {self.instructions}\n\n"
            f"Query: {query}\n\n"
            f"This query requires using one or more tools. Select all appropriate tools from the following:\n"
            f"{tool_descriptions}\n\n"
            "Output ALL necessary tool calls, each in the format:\n"
            "[TOOL]{\"name\":\"tool_name\",\"args\":{\"param\":\"value\"}}[/TOOL]\n"
            "If multiple tools are needed, include multiple [TOOL] tags, one per tool."
        )
        return direct_tool_prompt
    
    def run(self, query: str) -> Dict[str, Any]:
        trace_id = self.logger.trace_start("agent_run", {"query": query})

        has_any_tools = bool(self.tool_registry.get_all())
        relevant_tools = self._find_relevant_tools(query) if has_any_tools else []

        prompt = self._build_enhanced_prompt(query, relevant_tools)
        self.logger.trace_step(trace_id, "build_prompt", {"final_prompt_summary": prompt[:300] + "..."})

        thinking = None
        if self.thinking_enabled:
            thinking_prompt = (
                f"Instructions: {self.instructions}\n\n"
                f"Think step-by-step about how to answer this query: {query}\n\n"
                f"Available tools: {', '.join([t.name for t in self.tool_registry.get_all()]) if has_any_tools else 'None'}\n"
                "Determine if any tools are necessary to answer this query accurately. If multiple tools are needed, specify which ones and why."
            )
            try:
                thinking = self.call(thinking_prompt)
                self.logger.trace_step(trace_id, "thinking_complete", {"thinking": thinking})
            except Exception as e:
                self.logger.trace_error(trace_id, e, "Thinking phase failed")
                thinking = "Thinking phase failed due to error."

        messages = [{"role": "user", "content": prompt}]
        if thinking:
            messages.append({"role": "assistant", "content": f"Thinking: {thinking}"})
            messages.append({"role": "user", "content": "Now provide your final answer, using tools as specified in your thinking and the instructions."})

        self.logger.trace_step(trace_id, "generate_initial_llm_response", {"messages_count": len(messages)})
        llm_response_text = ""
        try:
            llm_response_text = self.chat(messages)
            self.logger.log(f"Initial LLM response: {llm_response_text[:200]}...")
        except Exception as e:
            self.logger.trace_error(trace_id, e, "Failed to generate initial response from LLM")
            if self.strict_tool_usage:
                llm_response_text = "Error: LLM provider failed to generate a response. Unable to proceed in strict tool usage mode."
            else:
                llm_response_text = "Error: LLM provider failed to generate a response."

        tool_calls = self._parse_tool_usage(llm_response_text, query)
        tool_outputs = []
        final_response = None

        if not has_any_tools and self.strict_tool_usage:
            final_response = "I am configured for strict tool usage, but no tools are available. I cannot answer your query."
            self.logger.log("Strict mode with no tools: responding with 'cannot answer'.")
        elif has_any_tools:
            if not tool_calls and self.strict_tool_usage:
                self.logger.log("Strict mode: No tools parsed from initial LLM response. Attempting direct tool selection.")
                direct_selection_tools = relevant_tools if relevant_tools else self.tool_registry.get_all()
                if direct_selection_tools:
                    direct_tool_prompt = self._create_direct_tool_prompt(query, direct_selection_tools)
                    self.logger.trace_step(trace_id, "direct_tool_prompt", {"prompt_summary": direct_tool_prompt[:200] + "..."})
                    try:
                        tool_call_response = self.call(direct_tool_prompt)
                        tool_calls = self._parse_tool_usage(tool_call_response, query)
                        if tool_calls:
                            self.logger.log(f"Tools identified via direct prompt: {[name for name, _ in tool_calls]}")
                        else:
                            self.logger.log("Direct tool prompt did not yield valid tool calls.")
                    except Exception as e:
                        self.logger.trace_error(trace_id, e, "Direct tool prompt LLM call failed")
                        if self.strict_tool_usage:
                            final_response = "I was unable to select appropriate tools for your query. Therefore, I cannot answer in strict tool usage mode."

            if tool_calls:
                for tool_name, tool_args in tool_calls:
                    cache_key = f"{tool_name}:{orjson.dumps(tool_args).decode('utf-8')}"
                    if cache_key in self.tool_cache:
                        tool_output = self.tool_cache[cache_key]
                        self.logger.trace_step(trace_id, "tool_cache_hit", {"tool": tool_name, "output": tool_output[:100] + "..." if len(tool_output) > 100 else tool_output})
                    else:
                        self.logger.trace_step(trace_id, "tool_usage_identified", {"tool": tool_name, "args": tool_args})
                        tool = self.tool_registry.get(tool_name)
                        if tool:
                            self.logger.trace_step(trace_id, "execute_tool_start", {"tool": tool_name})
                            if tool_name == "pdf_rag" and "query" not in tool_args and query:
                                tool_args["query"] = query
                                self.logger.log(f"Automatically set 'query' arg for pdf_rag tool to: {query[:50]}...")

                            try:
                                tool_output = tool.execute(tool_args)
                                self.tool_cache[cache_key] = tool_output
                                self.logger.trace_step(trace_id, "execute_tool_complete", {
                                    "output_preview": str(tool_output)[:100] + "..." if tool_output else "None"
                                })
                                tool_outputs.append((tool_name, tool_args, tool_output))
                            except Exception as e:
                                self.logger.trace_error(trace_id, e, f"Tool {tool_name} execution failed catastrophically.")
                                tool_output = f"Critical Error executing tool {tool_name}: {str(e)}"
                                tool_outputs.append((tool_name, tool_args, tool_output))
                                if self.strict_tool_usage:
                                    final_response = f"An error occurred while trying to use the {tool_name} tool: {str(e)}. Therefore, I cannot answer your query."
                                    break
                        else:
                            self.logger.log(f"Tool '{tool_name}' was identified by LLM but not found in the registry.")
                            tool_output = f"Error: The LLM suggested using a tool named '{tool_name}', but it is not available."
                            tool_outputs.append((tool_name, tool_args, tool_output))
                            if self.strict_tool_usage:
                                final_response = f"I identified a potential need for a tool named '{tool_name}', but it's not registered. I cannot answer your query without an appropriate tool."
                                break

                if not final_response:
                    final_response_prompt_parts = [
                        f"Instructions: {self.instructions}\n\n",
                        f"Original query: \"{query}\"\n\n"
                    ]
                    for tool_name, tool_args, tool_output in tool_outputs:
                        final_response_prompt_parts.append(
                            f"You used the '{tool_name}' tool with arguments: {tool_args}\n"
                            f"Tool output:\n---\n{tool_output}\n---\n\n"
                        )
                    final_response_prompt_parts.append(
                        "Based ONLY on the provided tool outputs and your primary instructions, formulate the final response to the original query. "
                        "Integrate the information from all tool outputs to address the original query comprehensively in a single paragraph."
                    )
                    if self.strict_tool_usage:
                        final_response_prompt_parts.append(
                            " You MUST NOT use any general knowledge beyond the tool outputs. "
                            "If any tool failed or did not provide sufficient information, indicate that in your response, but still provide as much information as possible from the successful tools."
                        )
                    else:
                        final_response_prompt_parts.append(
                            "If the tool outputs are insufficient, you may supplement with your general knowledge if appropriate, but prioritize the tools' findings."
                        )

                    final_response_prompt = "".join(final_response_prompt_parts)
                    self.logger.trace_step(trace_id, "final_response_prompt_after_tools", {"prompt_summary": final_response_prompt[:300] + "..."})
                    try:
                        final_response = self.call(final_response_prompt)
                    except Exception as e:
                        self.logger.trace_error(trace_id, e, "LLM call for final response generation after tool use failed.")
                        if self.strict_tool_usage:
                            final_response = f"I encountered an issue processing the results from the tools: {', '.join([name for name, _, _ in tool_outputs])}. I cannot provide an answer based on them."
                        else:
                            final_response = f"Error processing tool outputs: {[str(output)[:200] for _, _, output in tool_outputs]}"

            if not final_response and self.strict_tool_usage:
                self.logger.log("Strict mode: No tools were ultimately selected or used.")
                final_response = "I am configured to use specific tools for your query, but I was unable to identify or successfully use appropriate tools. Therefore, I cannot answer your request at this time."

        if not final_response:
            if self.strict_tool_usage:
                final_response = "I am configured for strict tool usage, but no tool was used or the process failed. I cannot answer your query."
            else:
                final_response = llm_response_text

        self.memory.add_turn(query, final_response, ", ".join([name for name, _, _ in tool_outputs]) if tool_outputs else None, "\n".join([str(output) for _, _, output in tool_outputs]) if tool_outputs else None)

        result = {
            "response": final_response,
            "thinking": thinking,
            "tools_used": [(name, args) for name, args, _ in tool_outputs] if tool_outputs else [],
            "tool_outputs": tool_outputs
        }

        self.logger.trace_end(trace_id, result)
        return result

    async def run_async(self, query: str) -> Dict[str, Any]:
        trace_id = self.logger.trace_start("agent_run_async", {"query": query})

        has_any_tools = bool(self.tool_registry.get_all())
        relevant_tools = self._find_relevant_tools(query) if has_any_tools else []

        prompt = self._build_enhanced_prompt(query, relevant_tools)
        self.logger.trace_step(trace_id, "build_prompt_async", {"final_prompt_summary": prompt[:300] + "..."})

        thinking = None
        if self.thinking_enabled:
            thinking_prompt = (
                f"Instructions: {self.instructions}\n\n"
                f"Think step-by-step about how to answer this query: {query}\n\n"
                f"Available tools: {', '.join([t.name for t in self.tool_registry.get_all()]) if has_any_tools else 'None'}\n"
                "Determine if any tools are necessary to answer this query accurately. If multiple tools are needed, specify which ones and why."
            )
            try:
                thinking = await self.call_async(thinking_prompt)
                self.logger.trace_step(trace_id, "thinking_complete_async", {"thinking": thinking})
            except Exception as e:
                self.logger.trace_error(trace_id, e, "Async thinking phase failed")
                thinking = "Async thinking phase failed due to error."

        messages = [{"role": "user", "content": prompt}]
        if thinking:
            messages.append({"role": "assistant", "content": f"Thinking: {thinking}"})
            messages.append({"role": "user", "content": "Now provide your final answer, using tools as specified in your thinking and the instructions."})

        self.logger.trace_step(trace_id, "generate_initial_llm_response_async", {"messages_count": len(messages)})
        llm_response_text = ""
        try:
            llm_response_text = await self.chat_async(messages)
            self.logger.log(f"Initial async LLM response: {llm_response_text[:200]}...")
        except Exception as e:
            self.logger.trace_error(trace_id, e, "Failed to generate initial async response from LLM")
            if self.strict_tool_usage:
                llm_response_text = "Error: LLM provider failed to generate an async response. Unable to proceed in strict tool usage mode."
            else:
                llm_response_text = "Error: LLM provider failed to generate an async response."

        tool_calls = self._parse_tool_usage(llm_response_text, query)
        tool_outputs = []
        final_response = None

        if not has_any_tools and self.strict_tool_usage:
            final_response = "I am configured for strict tool usage, but no tools are available. I cannot answer your query."
            self.logger.log("Strict mode with no tools (async): responding with 'cannot answer'.")
        elif has_any_tools:
            if not tool_calls and self.strict_tool_usage:
                self.logger.log("Strict mode (async): No tools parsed. Attempting direct tool selection.")
                direct_selection_tools = relevant_tools if relevant_tools else self.tool_registry.get_all()
                if direct_selection_tools:
                    direct_tool_prompt = self._create_direct_tool_prompt(query, direct_selection_tools)
                    self.logger.trace_step(trace_id, "direct_tool_prompt_async", {"prompt_summary": direct_tool_prompt[:200] + "..."})
                    try:
                        tool_call_response = await self.call_async(direct_tool_prompt)
                        tool_calls = self._parse_tool_usage(tool_call_response, query)
                        if tool_calls:
                            self.logger.log(f"Tools identified via async direct prompt: {[name for name, _ in tool_calls]}")
                        else:
                            self.logger.log("Async direct tool prompt did not yield valid tool calls.")
                    except Exception as e:
                        self.logger.trace_error(trace_id, e, "Async direct tool prompt LLM call failed")
                        if self.strict_tool_usage:
                            final_response = "I was unable to select appropriate tools for your query. Therefore, I cannot answer in strict tool usage mode."

            if tool_calls:
                for tool_name, tool_args in tool_calls:
                    cache_key = f"{tool_name}:{orjson.dumps(tool_args).decode('utf-8')}"
                    if cache_key in self.tool_cache:
                        tool_output = self.tool_cache[cache_key]
                        self.logger.trace_step(trace_id, "tool_cache_hit", {"tool": tool_name, "output": tool_output[:100] + "..." if len(tool_output) > 100 else tool_output})
                    else:
                        self.logger.trace_step(trace_id, "tool_usage_identified_async", {"tool": tool_name, "args": tool_args})
                        tool = self.tool_registry.get(tool_name)
                        if tool:
                            self.logger.trace_step(trace_id, "execute_tool_start_async", {"tool": tool_name})
                            if tool_name == "pdf_rag" and "query" not in tool_args and query:
                                tool_args["query"] = query
                                self.logger.log(f"Automatically set 'query' arg for pdf_rag tool (async) to: {query[:50]}...")
                            try:
                                if hasattr(tool, 'execute_async'):
                                    tool_output = await tool.execute_async(tool_args)
                                else:
                                    loop = asyncio.get_event_loop()
                                    tool_output = await loop.run_in_executor(None, lambda: tool.execute(tool_args))
                                self.tool_cache[cache_key] = tool_output
                                self.logger.trace_step(trace_id, "execute_tool_complete_async", {
                                    "output_preview": str(tool_output)[:100] + "..." if tool_output else "None"
                                })
                                tool_outputs.append((tool_name, tool_args, tool_output))
                            except Exception as e:
                                self.logger.trace_error(trace_id, e, f"Tool {tool_name} async execution failed.")
                                tool_output = f"Critical Error executing tool {tool_name} (async): {str(e)}"
                                tool_outputs.append((tool_name, tool_args, tool_output))
                                if self.strict_tool_usage:
                                    final_response = f"An error occurred while trying to use the {tool_name} tool (async): {str(e)}. Therefore, I cannot answer your query."
                                    break
                        else:
                            self.logger.log(f"Tool '{tool_name}' (async) identified but not found.")
                            tool_output = f"Error: Tool '{tool_name}' (async) is not recognized."
                            tool_outputs.append((tool_name, tool_args, tool_output))
                            if self.strict_tool_usage:
                                final_response = f"I identified a need for tool '{tool_name}' (async), but it's not available. I cannot answer."
                                break

                if not final_response:
                    final_response_prompt_parts = [
                        f"Instructions: {self.instructions}\n\n",
                        f"Original query: \"{query}\"\n\n"
                    ]
                    for tool_name, tool_args, tool_output in tool_outputs:
                        final_response_prompt_parts.append(
                            f"You used the '{tool_name}' tool with arguments: {tool_args}\n"
                            f"Tool output:\n---\n{tool_output}\n---\n\n"
                        )
                    final_response_prompt_parts.append(
                        "Based ONLY on the provided tool outputs and your primary instructions, formulate the final response to the original query. "
                        "Integrate the information from all tool outputs to address the original query comprehensively in a single paragraph."
                    )
                    if self.strict_tool_usage:
                        final_response_prompt_parts.append(
                            " You MUST NOT use any general knowledge beyond the tool outputs. "
                            "If any tool failed or did not provide sufficient information, indicate that in your response, but still provide as much information as possible from the successful tools."
                        )
                    else:
                        final_response_prompt_parts.append(
                            "If the tool outputs are insufficient, you may supplement with your general knowledge if appropriate, but prioritize the tools' findings."
                        )
                    
                    final_response_prompt = "".join(final_response_prompt_parts)
                    self.logger.trace_step(trace_id, "final_response_prompt_after_tools_async", {"prompt_summary": final_response_prompt[:300] + "..."})
                    try:
                        final_response = await self.call_async(final_response_prompt)
                    except Exception as e:
                        self.logger.trace_error(trace_id, e, "Async LLM call for final response generation failed.")
                        if self.strict_tool_usage:
                            final_response = f"I encountered an issue processing the results from the tools (async): {', '.join([name for name, _, _ in tool_outputs])}. I cannot provide an answer based on them."
                        else:
                            final_response = f"Error processing tool outputs (async): {[str(output)[:200] for _, _, output in tool_outputs]}"

            if not final_response and self.strict_tool_usage:
                self.logger.log("Strict mode (async): No tools were ultimately selected/used.")
                final_response = "I am configured for strict tool usage (async), but was unable to identify/use appropriate tools. Therefore, I cannot answer."

        if not final_response:
            if self.strict_tool_usage:
                final_response = "I am configured for strict tool usage (async), but no tool was used or the process failed. I cannot answer your query."
            else:
                final_response = llm_response_text
        self.memory.add_turn(query, final_response, ", ".join([name for name, _, _ in tool_outputs]) if tool_outputs else None, "\n".join([str(output) for _, _, output in tool_outputs]) if tool_outputs else None)

        result = {
            "response": final_response,
            "thinking": thinking,
            "tools_used": [(name, args) for name, args, _ in tool_outputs] if tool_outputs else [],
            "tool_outputs": tool_outputs
        }

        self.logger.trace_end(trace_id, result)
        return result
    
    def chain(self, query: str, max_steps: int = 5) -> Dict[str, Any]:
        trace_id = self.logger.trace_start("agent_chain", {
            "query": query,
            "max_steps": max_steps
        })
        
        steps = []
        current_query = query
        
        for step in range(max_steps):
            self.logger.trace_step(trace_id, f"chain_step_{step+1}", {"current_query": current_query})
            
            try:
                result = self.run(current_query)
                steps.append(result)
                
                if not result.get("tools_used"):
                    self.logger.trace_step(trace_id, "chain_complete_no_tool", {
                        "step": step + 1,
                        "reason": "No tools used, final answer reached"
                    })
                    break
                tool_outputs = result.get("tool_outputs")
                if not tool_outputs or any(output.startswith("Error") for _, _, output in tool_outputs):
                    self.logger.trace_step(trace_id, "chain_complete_no_output", {
                        "step": step + 1,
                        "reason": "Tools used but no valid output produced"
                    })
                    break
                
                current_query = f"Previous query: {current_query}\nTool outputs: {[str(output) for _, _, output in tool_outputs]}\nContinue reasoning and provide a final answer."
                
                self.logger.trace_step(trace_id, f"updated_query_step_{step+1}", {
                    "updated_query": current_query
                })
            except Exception as e:
                self.logger.trace_error(trace_id, e, f"Chain step {step+1} failed")
                steps.append({"response": f"Error in chain step {step+1}: {str(e)}"})
                break
        
        final_result = {
            "response": steps[-1]["response"] if steps else "Error: No steps completed",
            "steps": steps,
            "num_steps": len(steps)
        }
        
        self.logger.trace_end(trace_id, {
            "final_response": final_result["response"][:100] + "..." if len(final_result["response"]) > 100 else final_result["response"],
            "num_steps": len(steps)
        })
        
        return final_result

    async def chain_async(self, query: str, max_steps: int = 5) -> Dict[str, Any]:
        trace_id = self.logger.trace_start("agent_chain_async", {
            "query": query,
            "max_steps": max_steps
        })
        
        steps = []
        current_query = query
        
        for step in range(max_steps):
            self.logger.trace_step(trace_id, f"chain_step_{step+1}", {"current_query": current_query})
            
            try:
                result = await self.run_async(current_query)
                steps.append(result)
                
                if not result.get("tools_used"):
                    self.logger.trace_step(trace_id, "chain_complete_no_tool", {
                        "step": step + 1,
                        "reason": "No tools used, final answer reached"
                    })
                    break
                
                tool_outputs = result.get("tool_outputs")
                if not tool_outputs or any(output.startswith("Error") for _, _, output in tool_outputs):
                    self.logger.trace_step(trace_id, "chain_complete_no_output", {
                        "step": step + 1,
                        "reason": "Tools used but no valid output produced"
                    })
                    break
                
                current_query = f"Previous query: {current_query}\nTool outputs: {[str(output) for _, _, output in tool_outputs]}\nContinue reasoning and provide a final answer."
                
                self.logger.trace_step(trace_id, f"updated_query_step_{step+1}", {
                    "updated_query": current_query
                })
            except Exception as e:
                self.logger.trace_error(trace_id, e, f"Chain step {step+1} failed")
                steps.append({"response": f"Error in chain step {step+1}: {str(e)}"})
                break
        
        final_result = {
            "response": steps[-1]["response"] if steps else "Error: No steps completed",
            "steps": steps,
            "num_steps": len(steps)
        }
        
        self.logger.trace_end(trace_id, {
            "final_response": final_result["response"][:100] + "..." if len(final_result["response"]) > 100 else final_result["response"],
            "num_steps": len(steps)
        })
        
        return final_result
    
    def batch(self, queries: List[str]) -> List[Dict[str, Any]]:
        trace_id = self.logger.trace_start("batch_processing", {
            "num_queries": len(queries)
        })
        
        results = []
        for i, query in enumerate(queries):
            self.logger.trace_step(trace_id, f"batch_query_{i+1}", {
                "query": query
            })
            
            try:
                result = self.run(query)
                results.append(result)
                
                self.logger.trace_step(trace_id, f"batch_result_{i+1}", {
                    "response": result["response"][:100] + "..." if len(result["response"]) > 100 else result["response"],
                    "tools_used": result.get("tools_used")
                })
            except Exception as e:
                self.logger.trace_error(trace_id, e, f"Batch query {i+1} failed")
                results.append({"response": f"Error processing query: {str(e)}"})
        
        self.logger.trace_end(trace_id, {
            "num_results": len(results)
        })
        
        return results

    async def batch_async(self, queries: List[str]) -> List[Dict[str, Any]]:
        trace_id = self.logger.trace_start("batch_processing_async", {
            "num_queries": len(queries)
        })
        
        tasks = [self.run_async(query) for query in queries]
        results = []
        for i, task in enumerate(await asyncio.gather(*tasks, return_exceptions=True)):
            if isinstance(task, Exception):
                self.logger.trace_error(trace_id, task, f"Batch query {i+1} failed")
                results.append({"response": f"Error processing query: {str(task)}"})
            else:
                results.append(task)
                self.logger.trace_step(trace_id, f"batch_result_{i+1}", {
                    "response": task["response"][:100] + "..." if len(task["response"]) > 100 else task["response"],
                    "tools_used": task.get("tools_used")
                })
        
        self.logger.trace_end(trace_id, {
            "num_results": len(results)
        })
        
        return results
        
    def visualize_trace(self, trace_id: int) -> str:
        trace = self.logger.get_trace(trace_id)
        if not trace:
            return "Invalid trace ID"
            
        output = [
            f"Trace #{trace_id}: {trace['action']}",
            f"Started: {trace['start_time']}",
            f"Duration: {trace.get('duration_ms', 'N/A'):.2f}ms" if trace.get('duration_ms') else "Duration: N/A",
            f"Errors: {len(trace.get('errors', []))}",
            "",
            "Inputs:",
            orjson.dumps(trace['inputs'], option=orjson.OPT_INDENT_2).decode('utf-8'),
            "",
            "Steps:"
        ]
        
        for i, step in enumerate(trace['steps']):
            output.append(f"  Step {i+1}: {step['name']} ({step['time']})")
            output.append(f"    {orjson.dumps(step['details'], option=orjson.OPT_INDENT_2).decode('utf-8')}")
        
        if trace.get("errors"):
            output.append("")
            output.append("Errors:")
            for i, error in enumerate(trace["errors"]):
                output.append(f"  Error {i+1}: {error['context']} ({error['time']})")
                output.append(f"    Type: {error['error_type']}")
                output.append(f"    Message: {error['error_message']}")
                output.append(f"    Stack Trace:\n      {'      '.join(error['stack_trace'])}")
        
        output.extend([
            "",
            "Outputs:",
            orjson.dumps(trace.get('outputs', {}), option=orjson.OPT_INDENT_2).decode('utf-8')
        ])
        
        return "\n".join(output)