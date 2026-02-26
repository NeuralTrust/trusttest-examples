"""Example demonstrating basic usage of OllamaClient for LLM completions."""

import asyncio
import os

from trusttest.llm_clients.base import RetryConfig
from trusttest.llm_clients.ollama_client import OllamaClient

os.environ["OLLAMA_HOST"] = "https://example.com"

client = OllamaClient(
    model="gemma3:1b", temperature=0.2, retry_config=RetryConfig(attempts=3)
)

response = asyncio.run(
    client.complete(
        "What is the capital of France?",
        system_prompt="You are a helpful assistant.",
    )
)

print(response)
