import json
import asyncio
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import aiohttp
import orjson
import re

from .agent import Agent
from .tools import ToolRegistry
from .logger import AILogger

class AgentManager:
    """Manages multiple specialized agents and routes tasks to them"""
    def __init__(self, llm_provider, agents=None, verbose=False, instructions: str = None, 
                 log_file: Optional[str] = None, structured_logging: bool = False, 
                 fallback_providers: Optional[List] = None):
        self.provider = llm_provider
        self.agents = {}
        self.history = []
        self.verbose = verbose
        self.instructions = instructions or (
            "Route queries to the most appropriate agent based on their expertise and available tools. "
            "Consider the query's intent, required knowledge, and tool capabilities."
        )
        self.logger = AILogger(
            name="AgentManager",
            verbose=verbose,
            log_file=log_file,
            structured_logging=structured_logging
        )
        self.fallback_providers = fallback_providers or []
        self.http_session = None
        self.tool_cache = {}  # Shared cache for tool outputs
        self.semaphore = asyncio.Semaphore(2)  # Reduced to 2 for API rate limit stability

        if agents:
            if isinstance(agents, list):
                for agent in agents:
                    self.add_agent(
                        name=agent.name,
                        agent=agent,
                        description=f"Agent specialized in {agent.name} tasks"
                    )
            elif isinstance(agents, dict):
                for name, agent_info in agents.items():
                    if isinstance(agent_info, dict):
                        self.add_agent(
                            name=name,
                            agent=agent_info.get("agent"),
                            description=agent_info.get("description", f"Agent specialized in {name} tasks")
                        )
                    else:
                        self.add_agent(
                            name=name,
                            agent=agent_info,
                            description=f"Agent specialized in {name} tasks"
                        )

    async def __aenter__(self):
        self.http_session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.http_session:
            await self.http_session.close()

    @classmethod
    def from_agents(cls, agents: List[Agent], llm_provider=None, verbose=False, 
                    instructions: str = None, log_file: Optional[str] = None, 
                    structured_logging: bool = False, 
                    fallback_providers: Optional[List] = None) -> 'AgentManager':
        if not llm_provider and agents:
            llm_provider = agents[0].provider
        manager = cls(
            llm_provider=llm_provider,
            verbose=verbose,
            instructions=instructions,
            log_file=log_file,
            structured_logging=structured_logging,
            fallback_providers=fallback_providers
        )
        for agent in agents:
            manager.add_agent(
                name=agent.name,
                agent=agent,
                description=f"Agent specialized in {agent.name} tasks"
            )
        return manager

    def set_verbose(self, verbose: bool = True) -> 'AgentManager':
        self.verbose = verbose
        self.logger.verbose = verbose
        for name, info in self.agents.items():
            info["agent"].set_verbose(verbose)
        self.logger.info(f"Verbose mode set to: {verbose}")
        return self

    def set_instructions(self, instructions: str) -> 'AgentManager':
        self.instructions = instructions
        self.logger.info(f"Updated routing instructions: {instructions[:50]}...")
        return self

    def add_agent(self, name: str, agent: Agent, description: str) -> 'AgentManager':
        self.agents[name] = {
            "agent": agent,
            "description": description
        }
        agent.name = name
        agent.set_verbose(self.verbose)
        # Inject shared cache into agent
        agent.tool_cache = self.tool_cache
        self.logger.info(f"Added agent: {name} - {description}")
        return self

    def _build_agent_descriptions(self) -> str:
        agent_descriptions = []
        for name, info in self.agents.items():
            tool_info = ""
            if agent := info["agent"]:
                if hasattr(agent, "tool_registry") and agent.tool_registry:
                    tools = agent.tool_registry.get_all()
                    if tools:
                        tool_names = [t.name for t in tools]
                        tool_info = f" (Tools: {', '.join(tool_names)})"
            agent_descriptions.append(f"- {name}: {info['description']}{tool_info}")
        return "\n".join(agent_descriptions)

    def _select_default_agent(self) -> str:
        preferred_agents = ["general_expert", "search_expert"]
        for agent in preferred_agents:
            if agent in self.agents:
                return agent
        return list(self.agents.keys())[0] if self.agents else None

    def _clean_and_parse_json(self, response: str, trace_id: int, context: str) -> List[Dict[str, str]]:
        """Advanced JSON parsing with robust cleaning and validation."""
        self.logger.debug(f"Raw response for {context}: {response[:200] + '...' if len(response) > 200 else response}")
        cleaned_response = response.strip()
        cleaned_response = re.sub(r'^```(?:json)?\n|\n```$', '', cleaned_response, flags=re.MULTILINE).strip()
        if not cleaned_response:
            self.logger.error(f"Empty response after cleaning for {context}")
            return []

        try:
            parsed = orjson.loads(cleaned_response)
            if not isinstance(parsed, list):
                self.logger.error(f"Parsed response is not a list for {context}: {parsed}")
                return []
            for item in parsed:
                if not (isinstance(item, dict) and "sub_query" in item and "agent" in item):
                    self.logger.error(f"Invalid sub-query structure for {context}: {item}")
                    return []
                if item["agent"] not in self.agents:
                    self.logger.warning(f"Invalid agent {item['agent']} in {context}, ignoring sub-query")
                    return []
            self.logger.debug(f"Successfully parsed JSON for {context}: {parsed}")
            return parsed
        except orjson.JSONDecodeError as e:
            self.logger.trace_error(trace_id, e, f"Direct JSON parsing failed for {context}")

        json_pattern = r'\[\s*\{.*?\}\s*\]'
        match = re.search(json_pattern, cleaned_response, re.DOTALL)
        if match:
            try:
                parsed = orjson.loads(match.group(0))
                if not isinstance(parsed, list):
                    self.logger.error(f"Extracted JSON is not a list for {context}: {parsed}")
                    return []
                for item in parsed:
                    if not (isinstance(item, dict) and "sub_query" in item and "agent" in item):
                        self.logger.error(f"Invalid extracted sub-query structure for {context}: {item}")
                        return []
                    if item["agent"] not in self.agents:
                        self.logger.warning(f"Invalid agent {item['agent']} in extracted {context}, ignoring sub-query")
                        return []
                self.logger.debug(f"Successfully parsed extracted JSON for {context}: {parsed}")
                return parsed
            except orjson.JSONDecodeError as e:
                self.logger.trace_error(trace_id, e, f"Extracted JSON parsing failed for {context}")

        try:
            entries = re.findall(r'\{\s*"sub_query"\s*:\s*"([^"]+)"\s*,\s*"agent"\s*:\s*"([^"]+)"\s*\}', cleaned_response)
            parsed = [{"sub_query": entry[0], "agent": entry[1]} for entry in entries if entry[1] in self.agents]
            if parsed:
                self.logger.debug(f"Manually parsed JSON for {context}: {parsed}")
                return parsed
            self.logger.error(f"Manual JSON parsing found no valid entries for {context}")
        except Exception as e:
            self.logger.trace_error(trace_id, e, f"Manual JSON parsing failed for {context}")

        self.logger.error(f"All JSON parsing attempts failed for {context}")
        return []

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((Exception,)),
        reraise=True
    )
    def route(self, query: str) -> Dict[str, Any]:
        trace_id = self.logger.trace_start("route_query", {"query": query[:100] + "..." if len(query) > 100 else query})
        if not self.agents:
            self.logger.error("No agents available to handle query")
            self.logger.trace_end(trace_id, {"error": "No agents available"})
            raise ValueError("No agents available")
        if len(self.agents) == 1:
            agent_name = list(self.agents.keys())[0]
            agent = self.agents[agent_name]["agent"]
            self.logger.info(f"Only one agent available, using: {agent_name}")
            try:
                result = agent.run(query)
                result["agent_used"] = agent_name
                self.history.append({
                    "query": query,
                    "agent": agent_name,
                    "response": result["response"],
                    "timestamp": datetime.now().isoformat()
                })
                self.logger.trace_step(trace_id, "agent_execution", {
                    "agent": agent_name,
                    "response": result["response"][:100] + "..." if len(result["response"]) > 100 else result["response"]
                })
                self.logger.trace_end(trace_id, result)
                return result
            except Exception as e:
                self.logger.trace_error(trace_id, e, f"Agent {agent_name} execution failed")
                raise Exception(f"Single agent {agent_name} failed: {str(e)}")
        agent_descriptions_text = self._build_agent_descriptions()
        routing_prompt = (
            f"Instructions: {self.instructions}\n\n"
            f"Query: {query}\n\n"
            "Available agents:\n"
            f"{agent_descriptions_text}\n\n"
            "Select the most appropriate agent to handle this query based on their expertise and tools. "
            "You MUST return only the agent name as a plain string (e.g., 'weather_expert'). "
            "Do not include any additional text, explanations, or formatting."
        )
        self.logger.trace_step(trace_id, "build_routing_prompt", {"prompt": routing_prompt[:200] + "..." if len(routing_prompt) > 200 else routing_prompt})
        selected_agent = None
        providers = [self.provider] + self.fallback_providers
        for provider in providers:
            try:
                self.logger.info(f"Attempting routing with provider: {type(provider).__name__}")
                selected_agent = provider.generate(routing_prompt).strip()
                self.logger.trace_step(trace_id, "routing_decision", {
                    "provider": type(provider).__name__,
                    "selected_agent": selected_agent
                })
                if selected_agent in self.agents:
                    break
                self.logger.warning(f"Invalid agent selected: {selected_agent}, retrying with next provider")
                selected_agent = None
            except Exception as e:
                self.logger.trace_error(trace_id, e, f"Routing with provider {type(provider).__name__} failed")
                continue
        if not selected_agent:
            self.logger.error("Failed to select a valid agent, falling back to default agent")
            selected_agent = self._select_default_agent()
            self.logger.trace_step(trace_id, "fallback_to_default_agent", {"selected_agent": selected_agent})
        agent = self.agents[selected_agent]["agent"]
        self.logger.info(f"Routing query to agent: {selected_agent}")
        try:
            result = agent.run(query)
            result["agent_used"] = selected_agent
            self.history.append({
                "query": query,
                "agent": selected_agent,
                "response": result["response"],
                "timestamp": datetime.now().isoformat()
            })
            self.logger.trace_step(trace_id, "agent_execution", {
                "agent": selected_agent,
                "response": result["response"][:100] + "..." if len(result["response"]) > 100 else result["response"]
            })
            self.logger.trace_end(trace_id, result)
            return result
        except Exception as e:
            self.logger.trace_error(trace_id, e, f"Agent {selected_agent} execution failed")
            raise Exception(f"Agent {selected_agent} failed: {str(e)}")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((Exception,)),
        reraise=True
    )
    async def route_async(self, query: str) -> Dict[str, Any]:
        trace_id = self.logger.trace_start("route_query_async", {"query": query[:100] + "..." if len(query) > 100 else query})
        if not self.agents:
            self.logger.error("No agents available to handle query")
            self.logger.trace_end(trace_id, {"error": "No agents available"})
            raise ValueError("No agents available")
        if len(self.agents) == 1:
            agent_name = list(self.agents.keys())[0]
            agent = self.agents[agent_name]["agent"]
            self.logger.info(f"Only one agent available, using: {agent_name}")
            try:
                result = await agent.run_async(query)
                result["agent_used"] = agent_name
                self.history.append({
                    "query": query,
                    "agent": agent_name,
                    "response": result["response"],
                    "timestamp": datetime.now().isoformat()
                })
                self.logger.trace_step(trace_id, "agent_execution", {
                    "agent": agent_name,
                    "response": result["response"][:100] + "..." if len(result["response"]) > 100 else result["response"]
                })
                self.logger.trace_end(trace_id, result)
                return result
            except Exception as e:
                self.logger.trace_error(trace_id, e, f"Agent {agent_name} execution failed")
                raise Exception(f"Single agent {agent_name} failed: {str(e)}")
        agent_descriptions_text = self._build_agent_descriptions()
        routing_prompt = (
            f"Instructions: {self.instructions}\n\n"
            f"Query: {query}\n\n"
            "Available agents:\n"
            f"{agent_descriptions_text}\n\n"
            "Select the most appropriate agent to handle this query based on their expertise and tools. "
            "You MUST return only the agent name as a plain string (e.g., 'weather_expert'). "
            "Do not include any additional text, explanations, or formatting."
        )
        self.logger.trace_step(trace_id, "build_routing_prompt", {"prompt": routing_prompt[:200] + "..." if len(routing_prompt) > 200 else routing_prompt})
        selected_agent = None
        providers = [self.provider] + self.fallback_providers
        for provider in providers:
            try:
                self.logger.info(f"Attempting async routing with provider: {type(provider).__name__}")
                selected_agent = (await provider.generate_async(routing_prompt)).strip()
                self.logger.trace_step(trace_id, "routing_decision", {
                    "provider": type(provider).__name__,
                    "selected_agent": selected_agent
                })
                if selected_agent in self.agents:
                    break
                self.logger.warning(f"Invalid agent selected: {selected_agent}, retrying with next provider")
                selected_agent = None
            except Exception as e:
                self.logger.trace_error(trace_id, e, f"Async routing with provider {type(provider).__name__} failed")
                continue
        if not selected_agent:
            self.logger.error("Failed to select a valid agent, falling back to default agent")
            selected_agent = self._select_default_agent()
            self.logger.trace_step(trace_id, "fallback_to_default_agent", {"selected_agent": selected_agent})
        agent = self.agents[selected_agent]["agent"]
        self.logger.info(f"Routing query to agent: {selected_agent}")
        try:
            result = await agent.run_async(query)
            result["agent_used"] = selected_agent
            self.history.append({
                "query": query,
                "agent": selected_agent,
                "response": result["response"],
                "timestamp": datetime.now().isoformat()
            })
            self.logger.trace_step(trace_id, "agent_execution", {
                "agent": selected_agent,
                "response": result["response"][:100] + "..." if len(result["response"]) > 100 else result["response"]
            })
            self.logger.trace_end(trace_id, result)
            return result
        except Exception as e:
            self.logger.trace_error(trace_id, e, f"Agent {selected_agent} execution failed")
            raise Exception(f"Agent {selected_agent} failed: {str(e)}")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((Exception,)),
        reraise=True
    )
    def collaborate(self, query: str, max_agents: int = 5, agent_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        trace_id = self.logger.trace_start("collaborate", {
            "query": query[:100] + "..." if len(query) > 100 else query,
            "max_agents": max_agents
        })
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(
                    self.collaborate_async(query, max_agents, agent_ids)
                )
                self.logger.trace_end(trace_id, {
                    "response": result["response"][:100] + "..." if len(result["response"]) > 100 else result["response"],
                    "agents_used": result["agents_used"]
                })
                return result
            finally:
                loop.close()
        except Exception as e:
            self.logger.trace_error(trace_id, e, "Synchronous collaboration failed")
            raise Exception(f"Collaboration failed: {str(e)}")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((Exception,)),
        reraise=True
    )
    async def collaborate_async(self, query: str, max_agents: int = 5, agent_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        trace_id = self.logger.trace_start("collaborate_async", {
            "query": query[:100] + "..." if len(query) > 100 else query,
            "max_agents": max_agents
        })

        async with self:  # Manage HTTP session
            if not self.agents:
                self.logger.error("No agents available for collaboration")
                self.logger.trace_end(trace_id, {"error": "No agents available"})
                raise ValueError("No agents available")

            # Generate dynamic instructions for the manager
            dynamic_instructions = self.generate_dynamic_instructions(query)
            self.instructions = dynamic_instructions if dynamic_instructions else self.instructions

            # Handle the case where specific agents are requested
            if agent_ids:
                # Filter to only include agents that exist in the manager
                valid_agent_ids = [aid for aid in agent_ids if aid in self.agents]
                if valid_agent_ids:
                    selected_agents = valid_agent_ids[:max_agents]
                    # Create synthetic sub-queries so each agent processes the full query
                    sub_queries = [{"sub_query": query, "agent": agent_id} for agent_id in selected_agents]
                    self.logger.info(f"Using explicitly requested agents: {', '.join(selected_agents)}")
                    self.logger.trace_step(trace_id, "using_explicit_agents", {"selected_agents": selected_agents})
                else:
                    self.logger.warning("None of the requested agent_ids exist, falling back to query splitting")
                    agent_ids = None  # Reset to use normal query splitting
            
            # Only do LLM-based query splitting if no valid agent_ids were provided
            if not agent_ids:
                # LLM-based query splitting and agent selection
                agent_descriptions_text = self._build_agent_descriptions()
                query_split_prompt = (
                    f"Instructions: {self.instructions}\n\n"
                    f"Query: {query}\n\n"
                    f"Available agents:\n{agent_descriptions_text}\n\n"
                    "Analyze the query and split it into distinct sub-queries, assigning each to the most appropriate agent based on their expertise and tools. "
                    "Return a JSON array where each item is an object with 'sub_query' (the sub-query text) and 'agent' (the agent name). "
                    "If the query cannot be split, return a single sub-query with the most suitable agent. "
                    "Ensure all selected agents exist in the provided list and match the sub-query's requirements. "
                    "The output MUST be valid JSON, enclosed in square brackets, with each item having 'sub_query' and 'agent' fields. "
                    "Identify distinct tasks by looking for conjunctions (e.g., 'and', 'also') or multiple intents. "
                    "If the query is ambiguous, assign it to the most general agent capable of handling it. "
                    "Examples:\n"
                    "Query: 'what's the weather in kollam now? and tell me about spur ai'\n"
                    "```json\n"
                    "[\n"
                    "  {\"sub_query\": \"what's the weather in kollam now?\", \"agent\": \"weather_expert\"},\n"
                    "  {\"sub_query\": \"tell me about spur ai\", \"agent\": \"search_expert\"}\n"
                    "]\n"
                    "```\n"
                    "Query: 'tell me about python programming'\n"
                    "```json\n"
                    "[\n"
                    "  {\"sub_query\": \"tell me about python programming\", \"agent\": \"search_expert\"}\n"
                    "]\n"
                    "```\n"
                    "Query: 'how to fix a car engine and book a flight to paris'\n"
                    "```json\n"
                    "[\n"
                    "  {\"sub_query\": \"how to fix a car engine\", \"agent\": \"general_expert\"},\n"
                    "  {\"sub_query\": \"book a flight to paris\", \"agent\": \"search_expert\"}\n"
                    "]\n"
                    "```\n"
                    "Query: 'Tell me about Aromal TR and what's the weather in Trivandrum?'\n"
                    "```json\n"
                    "[\n"
                    "  {\"sub_query\": \"Tell me about Aromal TR\", \"agent\": \"search_expert\"},\n"
                    "  {\"sub_query\": \"what's the weather in Trivandrum?\", \"agent\": \"weather_expert\"}\n"
                    "]\n"
                    "```\n"
                    "Return format:\n"
                    "```json\n"
                    "[\n"
                    "  {\"sub_query\": \"text\", \"agent\": \"agent_name\"},\n"
                    "  ...\n"
                    "]\n"
                    "```"
                )
                self.logger.trace_step(trace_id, "build_query_split_prompt", {
                    "prompt": query_split_prompt[:200] + "..." if len(query_split_prompt) > 200 else query_split_prompt
                })

                sub_queries = []
                providers = [self.provider] + self.fallback_providers
                for provider in providers:
                    try:
                        self.logger.info(f"Attempting query splitting with provider: {type(provider).__name__}")
                        response = await provider.generate_async(query_split_prompt)
                        sub_queries = self._clean_and_parse_json(response, trace_id, "primary query splitting")
                        if sub_queries:
                            self.logger.trace_step(trace_id, "query_split", {"sub_queries": sub_queries})
                            break
                        self.logger.warning(f"No valid sub-queries from {type(provider).__name__}, retrying with next provider")
                    except Exception as e:
                        self.logger.trace_error(trace_id, e, f"Query splitting with provider {type(provider).__name__} failed")
                        continue

                if not sub_queries:
                    self.logger.warning("Primary query splitting failed, attempting simplified prompt")
                    simplified_prompt = (
                        f"Instructions: {self.instructions}\n\n"
                        f"Query: {query}\n\n"
                        f"Available agents:\n{agent_descriptions_text}\n\n"
                        "Analyze the query and assign it to the most appropriate agent. "
                        "Return a JSON array with a single object containing 'sub_query' (the full query) and 'agent' (the agent name). "
                        "Ensure the selected agent exists and is suitable for the query. "
                        "The output MUST be valid JSON. "
                        "Example:\n"
                        "```json\n"
                        "[\n"
                        "  {\"sub_query\": \"full query text\", \"agent\": \"agent_name\"}\n"
                        "]\n"
                        "```\n"
                        "Return format:\n"
                        "```json\n"
                        "[\n"
                        "  {\"sub_query\": \"text\", \"agent\": \"agent_name\"}\n"
                        "]\n"
                        "```"
                    )
                    for provider in providers:
                        try:
                            self.logger.info(f"Attempting simplified query splitting with provider: {type(provider).__name__}")
                            response = await provider.generate_async(simplified_prompt)
                            sub_queries = self._clean_and_parse_json(response, trace_id, "simplified query splitting")
                            if sub_queries:
                                self.logger.trace_step(trace_id, "simplified_query_split", {"sub_queries": sub_queries})
                                break
                            self.logger.warning(f"No valid sub-queries from simplified prompt with {type(provider).__name__}")
                        except Exception as e:
                            self.logger.trace_error(trace_id, e, f"Simplified query splitting with provider {type(provider).__name__} failed")
                            continue

                if not sub_queries:
                    self.logger.error("All query splitting attempts failed, falling back to default agent")
                    default_agent = self._select_default_agent()
                    sub_queries = [{"sub_query": query, "agent": default_agent}]
                    self.logger.trace_step(trace_id, "fallback_to_default_query_split", {"sub_queries": sub_queries})

                # Get all unique agents from sub-queries
                selected_agents = list(dict.fromkeys(sq["agent"] for sq in sub_queries))[:max_agents]
            
            # Ensure all agents have queries to work with
            agent_queries = {agent: [] for agent in selected_agents}
            for sq in sub_queries:
                if sq["agent"] in selected_agents:
                    agent_queries[sq["agent"]].append(sq["sub_query"])
            
            # Make sure every selected agent has at least one query
            for agent_name in selected_agents:
                if not agent_queries[agent_name]:
                    agent_queries[agent_name].append(query)  # Give the full query to agents with no specific sub-queries
                    self.logger.info(f"Assigned full query to agent {agent_name} which had no specific sub-queries")

            self.logger.info(f"Selected agents for async collaboration: {', '.join(selected_agents)}")
            self.logger.trace_step(trace_id, "agents_selected", {"selected_agents": selected_agents})

            agent_timeouts = {}
            for agent_name in selected_agents:
                agent = self.agents[agent_name]["agent"]
                timeout = 30.0
                if hasattr(agent, "tool_registry") and agent.tool_registry:
                    tools = agent.tool_registry.get_all()
                    if any(tool.name in ["search", "get_weather"] for tool in tools):
                        timeout = 45.0
                agent_timeouts[agent_name] = timeout

            results = []
            tasks = []

            async def run_agent_with_semaphore(agent_name: str, agent: Agent, queries: List[str]) -> Dict[str, Any]:
                async with self.semaphore:
                    start_time = asyncio.get_event_loop().time()
                    try:
                        combined_query = " and ".join(queries)
                        result = await asyncio.wait_for(
                            self._run_agent_async_with_error_handling(agent, agent_name, combined_query, trace_id),
                            timeout=agent_timeouts[agent_name]
                        )
                        if result.get("tool_used") and result.get("tool_output"):
                            cache_key = f"{result['tool_used']}:{json.dumps(result['tool_output'], sort_keys=True)}"
                            self.tool_cache[cache_key] = result["tool_output"]
                        normalized_result = {
                            "agent": agent_name,
                            "agent_used": agent_name,
                            "response": result.get("response", "No response")[:1000],
                            "tool_used": result.get("tool_used"),
                            "tool_output": result.get("tool_output"),
                            "queries": queries
                        }
                        self.logger.debug(f"Agent {agent_name} completed in {asyncio.get_event_loop().time() - start_time:.2f}s")
                        return normalized_result
                    except asyncio.TimeoutError:
                        self.logger.error(f"Agent {agent_name} timed out after {agent_timeouts[agent_name]}s")
                        return {
                            "agent": agent_name,
                            "agent_used": agent_name,
                            "response": f"Error: Agent timed out",
                            "tool_used": None,
                            "tool_output": None,
                            "queries": queries
                        }
                    except Exception as e:
                        self.logger.trace_error(trace_id, e, f"Agent {agent_name} failed")
                        return {
                            "agent": agent_name,
                            "agent_used": agent_name,
                            "response": f"Error: Agent {agent_name} failed: {str(e)}",
                            "tool_used": None,
                            "tool_output": None,
                            "queries": queries
                        }

            for agent_name in selected_agents:
                agent = self.agents[agent_name]["agent"]
                queries = agent_queries[agent_name]
                self.logger.info(f"Scheduling async agent: {agent_name} with queries: {queries}")
                tasks.append(run_agent_with_semaphore(agent_name, agent, queries))

            synthesis_prompt_parts = [
                "You are tasked with combining the following agent responses into a single, concise, and coherent paragraph that addresses the original query comprehensively. "
                "Avoid redundancy, prioritize reliable data, and disregard erroneous responses unless they provide useful partial information. "
                "If an agent reports an error or times out, state that the information could not be retrieved for that part of the query but still provide any available data from other agents. "
                "Organize the response clearly, ensuring all parts of the original query are addressed in a narrative format without bullet points. "
                f"Original Query: {query}\n\nAgent Responses:\n"
            ]
            results = []

            for future in asyncio.as_completed(tasks):
                result = await future
                results.append(result)
                agent_name = result["agent"]
                response = result["response"][:1000]
                queries = result["queries"]
                synthesis_prompt_parts.append(f"Agent {agent_name} (for sub-queries: {', '.join(queries)}):\n{response}\n\n")
                self.logger.trace_step(trace_id, f"agent_{agent_name}_execution", {
                    "response": response[:100] + "..." if len(response) > 100 else response,
                    "queries": queries
                })

            synthesis_prompt = "".join(synthesis_prompt_parts)
            self.logger.trace_step(trace_id, "build_synthesis_prompt", {
                "prompt": synthesis_prompt[:200] + "..." if len(synthesis_prompt) > 200 else synthesis_prompt
            })

            async def try_synthesis(provider, prompt: str) -> Optional[str]:
                try:
                    self.logger.info(f"Attempting async synthesis with provider: {type(provider).__name__}")
                    response = await provider.generate_async(prompt)
                    self.logger.trace_step(trace_id, f"synthesis_{type(provider).__name__}", {
                        "response": response[:100] + "..." if len(response) > 100 else response
                    })
                    return response
                except Exception as e:
                    self.logger.trace_error(trace_id, e, f"Synthesis with {type(provider).__name__} failed")
                    return None

            synthesis_tasks = [try_synthesis(provider, synthesis_prompt) for provider in [self.provider] + self.fallback_providers]
            final_response = None
            for future in asyncio.as_completed(synthesis_tasks):
                response = await future
                if response:
                    final_response = response
                    break

            if not final_response:
                final_response = "No valid responses from agents"
                self.logger.error("All synthesis attempts failed")

            final_result = {
                "response": final_response,
                "agent_results": results,
                "agents_used": selected_agents,
                "sub_queries": sub_queries
            }

            self.history.append({
                "query": query,
                "agents": selected_agents,
                "response": final_response,
                "timestamp": datetime.now().isoformat()
            })

            self.logger.trace_end(trace_id, {
                "response": final_response[:100] + "..." if len(final_response) > 100 else final_response,
                "agents_used": selected_agents,
                "sub_queries": sub_queries
            })
            return final_result

    async def _run_agent_async_with_error_handling(self, agent: Agent, agent_name: str, query: str, trace_id: int) -> Dict[str, Any]:
        try:
            result = await agent.run_async(query)
            normalized_result = {
                "agent": agent_name,
                "agent_used": agent_name,
                "response": result.get("response", "No response"),
                "tool_used": result.get("tool_used"),
                "tool_output": result.get("tool_output")
            }
            self.logger.trace_step(trace_id, f"agent_{agent_name}_execution", {
                "agent": agent_name,
                "response": normalized_result["response"][:100] + "..." if len(normalized_result["response"]) > 100 else normalized_result["response"]
            })
            return normalized_result
        except Exception as e:
            self.logger.trace_error(trace_id, e, f"Agent {agent_name} execution failed")
            return {
                "agent": agent_name,
                "agent_used": agent_name,
                "response": f"Error: Agent {agent_name} failed: {str(e)}",
                "tool_used": None,
                "tool_output": None
            }

    def generate_dynamic_instructions(self, query: str) -> str:
        """Generate dynamic instructions for the manager based on the query and available agents."""
        agent_descriptions = self._build_agent_descriptions()
        prompt = (
            f"Query: {query}\n\n"
            f"Available agents:\n{agent_descriptions}\n\n"
            "Based on the query, determine the best way to split it into sub-queries and assign them to agents. "
            "Provide instructions on how to handle the query effectively, considering the agents' expertise and tools."
        )
        return self.provider.generate(prompt)