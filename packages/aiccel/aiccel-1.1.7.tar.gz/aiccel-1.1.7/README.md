# AIccel: Lightweight AI Agent Framework

AIccel is a Python library for building lightweight, customizable AI agents. It supports multiple LLM providers (OpenAI, Gemini, Groq), custom tools, and agent collaboration, making it ideal for automation, conversational bots, and task orchestration.

## Installation

```bash
pip install aiccel
```

## Tutorial 

Below are three basic examples to get started with AIccel.

### 1. Single Agent with Search Tool

Create a single agent that uses a search tool to find information.

```python
from aiccel import OpenAIProvider, Agent, ToolRegistry
from aiccel.tools import SearchTool

provider = OpenAIProvider(api_key="your-openai-api-key", model="gpt-4o-mini")

search_tool = SearchTool(api_key="your-serper-api-key")


tools = ToolRegistry(llm_provider=provider).register(search_tool)

agent = Agent(
    provider=provider,
    tools=[search_tool],
    name="SearchAgent",
    instructions="Use the search tool to find current information."
)


result = agent.run("What is Spur AI?")
print(result["response"])
```

This agent uses the `SearchTool` to fetch real-time information about "Spur AI" via the Serper API. Replace `your-openai-api-key` and `your-serper-api-key` with your actual API keys.

### 2. Multiple Agents collaboration

Create a group of agents that collaborate.

```python
from aiccel import OpenAIProvider, Agent, AgentManager, ToolRegistry
from aiccel.tools import SearchTool, WeatherTool
import asyncio

provider = OpenAIProvider(api_key="your-openai-api-key", model="gpt-4o-mini")

search_tool = SearchTool(api_key="your-serper-api-key")
weather_tool = WeatherTool(api_key="your-openweather-api-key")



tool_registry = ToolRegistry(llm_provider=provider)
tool_registry.register(search_tool).register(weather_tool)


search_agent = Agent(
    provider=provider,
    tools=[search_tool],
    name="SearchAgent",
    instructions="Use the search tool to find current information.",
    memory_type="buffer",
    max_memory_turns=10,
    max_memory_tokens=2000,
    verbose=True
)

weather_agent = Agent(
    provider=provider,
    tools=[weather_tool],
    name="WeatherAgent",
    instructions="Provide detailed weather information using the weather tool.",
    memory_type="summary",
    max_memory_turns=5,
    max_memory_tokens=1000,
    verbose=True
)

general_agent = Agent(
    provider=provider,
    tools=[search_tool, weather_tool],
    name="GeneralAgent",
    instructions="Answer queries using search or weather tools when needed.",
    memory_type="window",
    max_memory_turns=3,
    max_memory_tokens=500,
    verbose=True
)


manager = AgentManager(
    llm_provider=provider,
    agents={
        "search_expert": {"agent": search_agent, "description": "Handles web searches"},
        "weather_expert": {"agent": weather_agent, "description": "Handles weather queries"},
        "general_expert": {"agent": general_agent, "description": "Handles broad queries"}
    },
    instructions="Route queries to the best-suited agent based on the query content.",
    # logger=logger,
    verbose=True
)


result = manager.route("What is Spur AI?")
print(result["response"])
```

Two agents collaborate: one researches Paris attractions, and the other checks the weather. The `AgentManager` coordinates their efforts. Replace API keys as needed.

### 3. PDF RAG Agent for Document Queries

Create an agent that answers questions based on PDF documents using Retrieval-Augmented Generation (RAG).

```python
from aiccel import OpenAIProvider, Agent, ToolRegistry
from aiccel.pdf_rag_tool import PDFRAGTool
from aiccel.embeddings import OpenAIEmbeddingProvider
import os


provider = OpenAIProvider(api_key="your-openai-api-key", model="gpt-4o-mini")
embedding_provider = OpenAIEmbeddingProvider(api_key="your-openai-api-key", model="text-embedding-3-small")


pdf_rag_tool = PDFRAGTool(
    base_pdf_folder="./docs",
    base_vector_db_path="./vector_store",
    embedding_provider=embedding_provider,
    llm_provider=provider
)


tools = ToolRegistry(llm_provider=provider).register(pdf_rag_tool)


agent = Agent(
    provider=provider,
    tools=[pdf_rag_tool],
    name="PDFRAGAgent",
    instructions="Answer queries using the pdf_rag tool only.",
    strict_tool_usage=True
)


os.makedirs("./docs", exist_ok=True)
os.makedirs("./vector_store", exist_ok=True)


result = agent.run("What is the main topic of the document?")
print(result["response"])
```

This agent uses the `PDFRAGTool` to answer questions based on PDFs in the `./docs` folder. It creates embeddings and stores them in `./vector_store`. Place a PDF in `./docs` before running, and replace API keys.

## Next Steps

- Explore more tools in `aiccel.tools` (e.g., custom tools).
- Configure agent memory (`memory_type`, `max_memory_turns`) for conversation history.
- Check out the AIccel GitHub for advanced examples.

## License

MIT License