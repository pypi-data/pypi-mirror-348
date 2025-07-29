import orjson
import requests
import asyncio
import zlib
from typing import Dict, List, Any, Optional, Union
from aiohttp import ClientSession, ClientTimeout
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from cachetools import TTLCache
from .logger import AILogger

class LLMProvider:
    """Base class for LLM providers with caching and logging"""
    _response_cache = TTLCache(maxsize=1000, ttl=3600)  # Cache for API responses

    def __init__(self, verbose: bool = False, log_file: Optional[str] = None, structured_logging: bool = False):
        self.logger = AILogger(
            name=self.__class__.__name__,
            verbose=verbose,
            log_file=log_file,
            structured_logging=structured_logging
        )

    def generate(self, prompt: str, **kwargs) -> str:
        raise NotImplementedError

    async def generate_async(self, prompt: str, **kwargs) -> str:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: self.generate(prompt, **kwargs))

    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        raise NotImplementedError

    async def chat_async(self, messages: List[Dict[str, str]], **kwargs) -> str:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: self.chat(messages, **kwargs))

    def embed(self, text: Union[str, List[str]]) -> List[float]:
        raise NotImplementedError

    async def embed_async(self, text: Union[str, List[str]]) -> List[float]:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: self.embed(text))

class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: str, model: str, embedding_model: str = None, 
                 verbose: bool = False, log_file: Optional[str] = None, structured_logging: bool = False):
        super().__init__(verbose=verbose, log_file=log_file, structured_logging=structured_logging)
        self.api_key = api_key
        self.model = model
        self.embedding_model = embedding_model or "text-embedding-3-small"
        self.http_session = None

    async def __aenter__(self):
        self.http_session = ClientSession(timeout=ClientTimeout(total=30))
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.http_session:
            await self.http_session.close()

    def generate(self, prompt: str, **kwargs) -> str:
        cache_key = f"generate:{zlib.compress(prompt.encode('utf-8')).hex()}"
        if cache_key in self._response_cache:
            self.logger.log(f"Cache hit for prompt: {prompt[:50]}...")
            return self._response_cache[cache_key]
        
        trace_id = self.logger.trace_start("openai_generate", {"prompt": prompt[:100]})
        try:
            result = self.chat([{"role": "user", "content": prompt}], **kwargs)
            self._response_cache[cache_key] = result
            self.logger.trace_end(trace_id, {"response": result[:100]})
            return result
        except Exception as e:
            self.logger.trace_error(trace_id, e, "OpenAI generate failed")
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=0.5, min=2, max=8),
        retry=retry_if_exception_type((Exception,)),
        reraise=True
    )
    async def generate_async(self, prompt: str, **kwargs) -> str:
        cache_key = f"generate:{zlib.compress(prompt.encode('utf-8')).hex()}"
        if cache_key in self._response_cache:
            self.logger.log(f"Cache hit for async prompt: {prompt[:50]}...")
            return self._response_cache[cache_key]
        
        trace_id = self.logger.trace_start("openai_generate_async", {"prompt": prompt[:100]})
        try:
            result = await self.chat_async([{"role": "user", "content": prompt}], **kwargs)
            self._response_cache[cache_key] = result
            self.logger.trace_end(trace_id, {"response": result[:100]})
            return result
        except Exception as e:
            self.logger.trace_error(trace_id, e, "OpenAI async generate failed")
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=0.5, min=2, max=8),
        retry=retry_if_exception_type((requests.exceptions.RequestException, requests.exceptions.HTTPError)),
        reraise=True
    )
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        trace_id = self.logger.trace_start("openai_chat", {"message_count": len(messages)})
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": kwargs.get("temperature", 0.7),
            "max_tokens": kwargs.get("max_tokens", 2048)
        }
        
        data = {k: v for k, v in data.items() if v is not None}
        cache_key = f"chat:{zlib.compress(orjson.dumps(data, option=orjson.OPT_SORT_KEYS)).hex()}"
        if cache_key in self._response_cache:
            self.logger.log("Cache hit for chat messages")
            return self._response_cache[cache_key]
        
        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            response_json = orjson.loads(response.content)
            if not response_json.get("choices") or not response_json["choices"][0].get("message"):
                raise Exception("Invalid response format: Missing choices or message")
            result = response_json["choices"][0]["message"]["content"]
            self._response_cache[cache_key] = result
            self.logger.trace_end(trace_id, {"response": result[:100]})
            return result
        except requests.exceptions.HTTPError as e:
            error_msg = f"OpenAI API error ({e.response.status_code}): {e.response.text}"
            if e.response.status_code in [401, 403]:
                self.logger.trace_error(trace_id, e, error_msg)
                raise Exception(error_msg)
            elif e.response.status_code == 429:
                self.logger.trace_error(trace_id, e, "Rate limit exceeded")
                raise Exception("Rate limit exceeded. Please try again later.")
            raise Exception(error_msg)
        except requests.exceptions.RequestException as e:
            error_msg = f"OpenAI network error: {str(e)}"
            self.logger.trace_error(trace_id, e, error_msg)
            raise Exception(error_msg)
        except Exception as e:
            error_msg = f"OpenAI response parsing error: {str(e)}"
            self.logger.trace_error(trace_id, e, error_msg)
            raise Exception(error_msg)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=0.5, min=2, max=8),
        retry=retry_if_exception_type((Exception,)),
        reraise=True
    )
    async def chat_async(self, messages: List[Dict[str, str]], **kwargs) -> str:
        trace_id = self.logger.trace_start("openai_chat_async", {"message_count": len(messages)})
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": kwargs.get("temperature", 0.7),
            "max_tokens": kwargs.get("max_tokens", 2048)
        }
        
        data = {k: v for k, v in data.items() if v is not None}
        cache_key = f"chat:{zlib.compress(orjson.dumps(data, option=orjson.OPT_SORT_KEYS)).hex()}"
        if cache_key in self._response_cache:
            self.logger.log("Cache hit for async chat messages")
            return self._response_cache[cache_key]
        
        async with ClientSession(timeout=ClientTimeout(total=30)) as session:
            try:
                async with session.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers=headers,
                    json=data
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        if response.status in [401, 403]:
                            error_msg = f"OpenAI API error ({response.status}): {error_text}"
                            self.logger.trace_error(trace_id, None, error_msg)
                            raise Exception(error_msg)
                        elif response.status == 429:
                            error_msg = "Rate limit exceeded. Please try again later."
                            self.logger.trace_error(trace_id, None, error_msg)
                            raise Exception(error_msg)
                        error_msg = f"OpenAI API error ({response.status}): {error_text}"
                        self.logger.trace_error(trace_id, None, error_msg)
                        raise Exception(error_msg)
                    response_json = await response.json()
                    if not response_json.get("choices") or not response_json["choices"][0].get("message"):
                        error_msg = "Invalid response format: Missing choices or message"
                        self.logger.trace_error(trace_id, None, error_msg)
                        raise Exception(error_msg)
                    result = response_json["choices"][0]["message"]["content"]
                    self._response_cache[cache_key] = result
                    self.logger.trace_end(trace_id, {"response": result[:100]})
                    return result
            except Exception as e:
                error_msg = f"OpenAI async error: {str(e)}"
                self.logger.trace_error(trace_id, e, error_msg)
                raise Exception(error_msg)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=0.5, min=2, max=8),
        retry=retry_if_exception_type((requests.exceptions.RequestException, requests.exceptions.HTTPError)),
        reraise=True
    )
    def embed(self, text: Union[str, List[str]]) -> List[float]:
        trace_id = self.logger.trace_start("openai_embed", {"text_length": len(text) if isinstance(text, str) else len(text[0])})
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.embedding_model,
            "input": text
        }
        
        cache_key = f"embed:{zlib.compress(orjson.dumps(data, option=orjson.OPT_SORT_KEYS)).hex()}"
        if cache_key in self._response_cache:
            self.logger.log("Cache hit for embed text")
            return self._response_cache[cache_key]
        
        try:
            response = requests.post(
                "https://api.openai.com/v1/embeddings",
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            response_json = orjson.loads(response.content)
            if not response_json.get("data"):
                error_msg = "Invalid response format: Missing data"
                self.logger.trace_error(trace_id, None, error_msg)
                raise Exception(error_msg)
            if isinstance(text, str):
                result = response_json["data"][0]["embedding"]
            else:
                result = [item["embedding"] for item in response_json["data"]]
            self._response_cache[cache_key] = result
            self.logger.trace_end(trace_id, {"embedding_length": len(result)})
            return result
        except requests.exceptions.HTTPError as e:
            error_msg = f"OpenAI embedding error ({e.response.status_code}): {e.response.text}"
            if e.response.status_code in [401, 403]:
                self.logger.trace_error(trace_id, e, error_msg)
                raise Exception(error_msg)
            elif e.response.status_code == 429:
                error_msg = "Rate limit exceeded. Please try again later."
                self.logger.trace_error(trace_id, e, error_msg)
                raise Exception(error_msg)
            self.logger.trace_error(trace_id, e, error_msg)
            raise Exception(error_msg)
        except requests.exceptions.RequestException as e:
            error_msg = f"OpenAI embedding network error: {str(e)}"
            self.logger.trace_error(trace_id, e, error_msg)
            raise Exception(error_msg)
        except Exception as e:
            error_msg = f"OpenAI embedding parsing error: {str(e)}"
            self.logger.trace_error(trace_id, e, error_msg)
            raise Exception(error_msg)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=0.5, min=2, max=8),
        retry=retry_if_exception_type((Exception,)),
        reraise=True
    )
    async def embed_async(self, text: Union[str, List[str]]) -> List[float]:
        trace_id = self.logger.trace_start("openai_embed_async", {"text_length": len(text) if isinstance(text, str) else len(text[0])})
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.embedding_model,
            "input": text
        }
        
        cache_key = f"embed:{zlib.compress(orjson.dumps(data, option=orjson.OPT_SORT_KEYS)).hex()}"
        if cache_key in self._response_cache:
            self.logger.log("Cache hit for async embed text")
            return self._response_cache[cache_key]
        
        async with ClientSession(timeout=ClientTimeout(total=30)) as session:
            try:
                async with session.post(
                    "https://api.openai.com/v1/embeddings",
                    headers=headers,
                    json=data
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        error_msg = f"OpenAI embedding error ({response.status}): {error_text}"
                        if response.status in [401, 403]:
                            self.logger.trace_error(trace_id, None, error_msg)
                            raise Exception(error_msg)
                        elif response.status == 429:
                            error_msg = "Rate limit exceeded. Please try again later."
                            self.logger.trace_error(trace_id, None, error_msg)
                            raise Exception(error_msg)
                        self.logger.trace_error(trace_id, None, error_msg)
                        raise Exception(error_msg)
                    response_json = await response.json()
                    if not response_json.get("data"):
                        error_msg = "Invalid response format: Missing data"
                        self.logger.trace_error(trace_id, None, error_msg)
                        raise Exception(error_msg)
                    if isinstance(text, str):
                        result = response_json["data"][0]["embedding"]
                    else:
                        result = [item["embedding"] for item in response_json["data"]]
                    self._response_cache[cache_key] = result
                    self.logger.trace_end(trace_id, {"embedding_length": len(result)})
                    return result
            except Exception as e:
                error_msg = f"OpenAI async embedding error: {str(e)}"
                self.logger.trace_error(trace_id, e, error_msg)
                raise Exception(error_msg)

class GeminiProvider(LLMProvider):
    def __init__(self, api_key: str, model: str, embedding_provider: Optional[LLMProvider] = None, 
                 verbose: bool = False, log_file: Optional[str] = None, structured_logging: bool = False):
        super().__init__(verbose=verbose, log_file=log_file, structured_logging=structured_logging)
        self.api_key = api_key
        self.model = model
        self.embedding_provider = embedding_provider
        self.http_session = None

    async def __aenter__(self):
        self.http_session = ClientSession(timeout=ClientTimeout(total=30))
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.http_session:
            await self.http_session.close()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=0.5, min=2, max=8),
        retry=retry_if_exception_type((requests.exceptions.RequestException, requests.exceptions.HTTPError)),
        reraise=True
    )
    def generate(self, prompt: str, **kwargs) -> str:
        cache_key = f"generate:{zlib.compress(prompt.encode('utf-8')).hex()}"
        if cache_key in self._response_cache:
            self.logger.log(f"Cache hit for prompt: {prompt[:50]}...")
            return self._response_cache[cache_key]
        
        trace_id = self.logger.trace_start("gemini_generate", {"prompt": prompt[:100]})
        try:
            result = self.chat([{"role": "user", "content": prompt}], **kwargs)
            self._response_cache[cache_key] = result
            self.logger.trace_end(trace_id, {"response": result[:100]})
            return result
        except Exception as e:
            self.logger.trace_error(trace_id, e, "Gemini generate failed")
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=0.5, min=2, max=8),
        retry=retry_if_exception_type((Exception,)),
        reraise=True
    )
    async def generate_async(self, prompt: str, **kwargs) -> str:
        cache_key = f"generate:{zlib.compress(prompt.encode('utf-8')).hex()}"
        if cache_key in self._response_cache:
            self.logger.log(f"Cache hit for async prompt: {prompt[:50]}...")
            return self._response_cache[cache_key]
        
        trace_id = self.logger.trace_start("gemini_generate_async", {"prompt": prompt[:100]})
        try:
            result = await self.chat_async([{"role": "user", "content": prompt}], **kwargs)
            self._response_cache[cache_key] = result
            self.logger.trace_end(trace_id, {"response": result[:100]})
            return result
        except Exception as e:
            self.logger.trace_error(trace_id, e, "Gemini async generate failed")
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=0.5, min=2, max=8),
        retry=retry_if_exception_type((requests.exceptions.RequestException, requests.exceptions.HTTPError)),
        reraise=True
    )
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        trace_id = self.logger.trace_start("gemini_chat", {"message_count": len(messages)})
        url = f"https://generativelanguage.googleapis.com/v1/models/{self.model}:generateContent?key={self.api_key}"
        
        contents = []
        for msg in messages:
            role = "user" if msg["role"].lower() == "user" else "model"
            contents.append({
                "role": role,
                "parts": [{"text": msg["content"]}]
            })
        
        data = {
            "contents": contents,
            "generationConfig": {
                "temperature": kwargs.get("temperature", 0.7),
                "maxOutputTokens": kwargs.get("max_tokens", 2048),
            }
        }
        
        data["generationConfig"] = {k: v for k, v in data["generationConfig"].items() if v is not None}
        cache_key = f"chat:{zlib.compress(orjson.dumps(data, option=orjson.OPT_SORT_KEYS)).hex()}"
        if cache_key in self._response_cache:
            self.logger.log("Cache hit for chat messages")
            return self._response_cache[cache_key]
        
        try:
            response = requests.post(url, json=data, timeout=30)
            response.raise_for_status()
            response_json = orjson.loads(response.content)
            if not response_json.get("candidates") or not response_json["candidates"][0].get("content"):
                error_msg = "Invalid response format: Missing candidates or content"
                self.logger.trace_error(trace_id, None, error_msg)
                raise Exception(error_msg)
            result = response_json["candidates"][0]["content"]["parts"][0]["text"]
            self._response_cache[cache_key] = result
            self.logger.trace_end(trace_id, {"response": result[:100]})
            return result
        except requests.exceptions.HTTPError as e:
            error_msg = f"Gemini API error ({e.response.status_code}): {e.response.text}"
            if e.response.status_code in [401, 403]:
                self.logger.trace_error(trace_id, e, error_msg)
                raise Exception(error_msg)
            elif e.response.status_code == 429:
                error_msg = "Rate limit exceeded. Please try again later."
                self.logger.trace_error(trace_id, e, error_msg)
                raise Exception(error_msg)
            self.logger.trace_error(trace_id, e, error_msg)
            raise Exception(error_msg)
        except requests.exceptions.RequestException as e:
            error_msg = f"Gemini network error: {str(e)}"
            self.logger.trace_error(trace_id, e, error_msg)
            raise Exception(error_msg)
        except Exception as e:
            error_msg = f"Gemini response parsing error: {str(e)}"
            self.logger.trace_error(trace_id, e, error_msg)
            raise Exception(error_msg)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=0.5, min=2, max=8),
        retry=retry_if_exception_type((Exception,)),
        reraise=True
    )
    async def chat_async(self, messages: List[Dict[str, str]], **kwargs) -> str:
        trace_id = self.logger.trace_start("gemini_chat_async", {"message_count": len(messages)})
        url = f"https://generativelanguage.googleapis.com/v1/models/{self.model}:generateContent?key={self.api_key}"
        
        contents = []
        for msg in messages:
            role = "user" if msg["role"].lower() == "user" else "model"
            contents.append({
                "role": role,
                "parts": [{"text": msg["content"]}]
            })
        
        data = {
            "contents": contents,
            "generationConfig": {
                "temperature": kwargs.get("temperature", 0.7),
                "maxOutputTokens": kwargs.get("max_tokens", 2048),
            }
        }
        
        data["generationConfig"] = {k: v for k, v in data["generationConfig"].items() if v is not None}
        cache_key = f"chat:{zlib.compress(orjson.dumps(data, option=orjson.OPT_SORT_KEYS)).hex()}"
        if cache_key in self._response_cache:
            self.logger.log("Cache hit for async chat messages")
            return self._response_cache[cache_key]
        
        async with ClientSession(timeout=ClientTimeout(total=30)) as session:
            try:
                async with session.post(url, json=data) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        error_msg = f"Gemini API error ({response.status}): {error_text}"
                        if response.status in [401, 403]:
                            self.logger.trace_error(trace_id, None, error_msg)
                            raise Exception(error_msg)
                        elif response.status == 429:
                            error_msg = "Rate limit exceeded. Please try again later."
                            self.logger.trace_error(trace_id, None, error_msg)
                            raise Exception(error_msg)
                        self.logger.trace_error(trace_id, None, error_msg)
                        raise Exception(error_msg)
                    response_json = await response.json()
                    if not response_json.get("candidates") or not response_json["candidates"][0].get("content"):
                        error_msg = "Invalid response format: Missing candidates or content"
                        self.logger.trace_error(trace_id, None, error_msg)
                        raise Exception(error_msg)
                    result = response_json["candidates"][0]["content"]["parts"][0]["text"]
                    self._response_cache[cache_key] = result
                    self.logger.trace_end(trace_id, {"response": result[:100]})
                    return result
            except Exception as e:
                error_msg = f"Gemini async error: {str(e)}"
                self.logger.trace_error(trace_id, e, error_msg)
                raise Exception(error_msg)

    def embed(self, text: Union[str, List[str]]) -> List[float]:
        if not self.embedding_provider:
            error_msg = "No embedding provider specified. Please set embedding_provider when creating this provider."
            self.logger.log(error_msg)
            raise ValueError(error_msg)
        trace_id = self.logger.trace_start("gemini_embed", {"text_length": len(text) if isinstance(text, str) else len(text[0])})
        try:
            result = self.embedding_provider.embed(text)
            self.logger.trace_end(trace_id, {"embedding_length": len(result)})
            return result
        except Exception as e:
            self.logger.trace_error(trace_id, e, "Gemini embed failed")
            raise

    async def embed_async(self, text: Union[str, List[str]]) -> List[float]:
        if not self.embedding_provider:
            error_msg = "No embedding provider specified. Please set embedding_provider when creating this provider."
            self.logger.log(error_msg)
            raise ValueError(error_msg)
        trace_id = self.logger.trace_start("gemini_embed_async", {"text_length": len(text) if isinstance(text, str) else len(text[0])})
        try:
            result = await self.embedding_provider.embed_async(text)
            self.logger.trace_end(trace_id, {"embedding_length": len(result)})
            return result
        except Exception as e:
            self.logger.trace_error(trace_id, e, "Gemini async embed failed")
            raise

from typing import List, Dict, Union, Optional
from cachetools import TTLCache
import requests
import orjson
import zlib
from aiohttp import ClientSession, ClientTimeout
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from .logger import AILogger

class GroqProvider(LLMProvider):
    def __init__(self, api_key: str, model: str, embedding_provider: Optional[LLMProvider] = None, 
                 verbose: bool = False, log_file: Optional[str] = None, structured_logging: bool = False):
        super().__init__(verbose=verbose, log_file=log_file, structured_logging=structured_logging)
        self.api_key = api_key
        self.model = model
        self.embedding_provider = embedding_provider
        self.http_session = None
        self._response_cache = TTLCache(maxsize=1000, ttl=3600)

    async def __aenter__(self):
        self.http_session = ClientSession(timeout=ClientTimeout(total=30))
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.http_session:
            await self.http_session.close()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=0.5, min=2, max=8),
        retry=retry_if_exception_type((requests.exceptions.RequestException, requests.exceptions.HTTPError)),
        reraise=True
    )
    def generate(self, prompt: str, **kwargs) -> str:
        cache_key = f"generate:{zlib.compress(prompt.encode('utf-8')).hex()}"
        if cache_key in self._response_cache:
            self.logger.log(f"Cache hit for prompt: {prompt[:50]}...")
            return self._response_cache[cache_key]
        
        trace_id = self.logger.trace_start("groq_generate", {"prompt": prompt[:100]})
        try:
            result = self.chat([{"role": "user", "content": prompt}], **kwargs)
            self._response_cache[cache_key] = result
            self.logger.trace_end(trace_id, {"response": result[:100]})
            return result
        except Exception as e:
            self.logger.trace_error(trace_id, e, "Groq generate failed")
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=0.5, min=2, max=8),
        retry=retry_if_exception_type((Exception,)),
        reraise=True
    )
    async def generate_async(self, prompt: str, **kwargs) -> str:
        cache_key = f"generate:{zlib.compress(prompt.encode('utf-8')).hex()}"
        if cache_key in self._response_cache:
            self.logger.log(f"Cache hit for async prompt: {prompt[:50]}...")
            return self._response_cache[cache_key]
        
        trace_id = self.logger.trace_start("groq_generate_async", {"prompt": prompt[:100]})
        try:
            result = await self.chat_async([{"role": "user", "content": prompt}], **kwargs)
            self._response_cache[cache_key] = result
            self.logger.trace_end(trace_id, {"response": result[:100]})
            return result
        except Exception as e:
            self.logger.trace_error(trace_id, e, "Groq async generate failed")
            raise

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=0.5, min=2, max=8),
        retry=retry_if_exception_type((requests.exceptions.RequestException, requests.exceptions.HTTPError)),
        reraise=True
    )
    def chat(self, messages: List[Dict[str, str]], **kwargs) -> str:
        trace_id = self.logger.trace_start("groq_chat", {"message_count": len(messages)})
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": kwargs.get("temperature", 0.7),
            "max_tokens": kwargs.get("max_tokens", 2048)
        }
        
        data = {k: v for k, v in data.items() if v is not None}
        cache_key = f"chat:{zlib.compress(orjson.dumps(data, option=orjson.OPT_SORT_KEYS)).hex()}"
        if cache_key in self._response_cache:
            self.logger.log("Cache hit for chat messages")
            return self._response_cache[cache_key]
        
        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            response_json = orjson.loads(response.content)
            if not response_json.get("choices") or not response_json["choices"][0].get("message"):
                error_msg = "Invalid response format: Missing choices or message"
                self.logger.trace_error(trace_id, None, error_msg)
                raise Exception(error_msg)
            result = response_json["choices"][0]["message"]["content"]
            self._response_cache[cache_key] = result
            self.logger.trace_end(trace_id, {"response": result[:100]})
            return result
        except requests.exceptions.HTTPError as e:
            error_msg = f"Groq API error ({e.response.status_code}): {e.response.text}"
            if e.response.status_code in [401, 403]:
                self.logger.trace_error(trace_id, e, error_msg)
                raise Exception(error_msg)
            elif e.response.status_code == 429:
                error_msg = "Rate limit exceeded. Please try again later."
                self.logger.trace_error(trace_id, e, error_msg)
                raise Exception(error_msg)
            self.logger.trace_error(trace_id, e, error_msg)
            raise Exception(error_msg)
        except requests.exceptions.RequestException as e:
            error_msg = f"Groq network error: {str(e)}"
            self.logger.trace_error(trace_id, e, error_msg)
            raise Exception(error_msg)
        except Exception as e:
            error_msg = f"Groq response parsing error: {str(e)}"
            self.logger.trace_error(trace_id, e, error_msg)
            raise Exception(error_msg)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=0.5, min=2, max=8),
        retry=retry_if_exception_type((Exception,)),
        reraise=True
    )
    async def chat_async(self, messages: List[Dict[str, str]], **kwargs) -> str:
        trace_id = self.logger.trace_start("groq_chat_async", {"message_count": len(messages)})
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": kwargs.get("temperature", 0.7),
            "max_tokens": kwargs.get("max_tokens", 2048)
        }
        
        data = {k: v for k, v in data.items() if v is not None}
        cache_key = f"chat:{zlib.compress(orjson.dumps(data, option=orjson.OPT_SORT_KEYS)).hex()}"
        if cache_key in self._response_cache:
            self.logger.log("Cache hit for async chat messages")
            return self._response_cache[cache_key]
        
        async with ClientSession(timeout=ClientTimeout(total=30)) as session:
            try:
                async with session.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers=headers,
                    json=data
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        error_msg = f"Groq API error ({response.status}): {error_text}"
                        if response.status in [401, 403]:
                            self.logger.trace_error(trace_id, None, error_msg)
                            raise Exception(error_msg)
                        elif response.status == 429:
                            error_msg = "Rate limit exceeded. Please try again later."
                            self.logger.trace_error(trace_id, None, error_msg)
                            raise Exception(error_msg)
                        self.logger.trace_error(trace_id, None, error_msg)
                        raise Exception(error_msg)
                    response_json = await response.json()
                    if not response_json.get("choices") or not response_json["choices"][0].get("message"):
                        error_msg = "Invalid response format: Missing choices or message"
                        self.logger.trace_error(trace_id, None, error_msg)
                        raise Exception(error_msg)
                    result = response_json["choices"][0]["message"]["content"]
                    self._response_cache[cache_key] = result
                    self.logger.trace_end(trace_id, {"response": result[:100]})
                    return result
            except Exception as e:
                error_msg = f"Groq async error: {str(e)}"
                self.logger.trace_error(trace_id, e, error_msg)
                raise Exception(error_msg)

    def embed(self, text: Union[str, List[str]]) -> List[float]:
        if not self.embedding_provider:
            error_msg = "No embedding provider specified. Please set embedding_provider when creating this provider."
            self.logger.log(error_msg)
            raise ValueError(error_msg)
        trace_id = self.logger.trace_start("groq_embed", {"text_length": len(text) if isinstance(text, str) else len(text[0])})
        try:
            result = self.embedding_provider.embed(text)
            self.logger.trace_end(trace_id, {"embedding_length": len(result)})
            return result
        except Exception as e:
            self.logger.trace_error(trace_id, e, "Groq embed failed")
            raise

    async def embed_async(self, text: Union[str, List[str]]) -> List[float]:
        if not self.embedding_provider:
            error_msg = "No embedding provider specified. Please set embedding_provider when creating this provider."
            self.logger.log(error_msg)
            raise ValueError(error_msg)
        trace_id = self.logger.trace_start("groq_embed_async", {"text_length": len(text) if isinstance(text, str) else len(text[0])})
        try:
            result = await self.embedding_provider.embed_async(text)
            self.logger.trace_end(trace_id, {"embedding_length": len(result)})
            return result
        except Exception as e:
            self.logger.trace_error(trace_id, e, "Groq async embed failed")
            raise