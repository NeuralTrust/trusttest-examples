"""Example demonstrating Groq API usage with custom base URL using get_llm_client."""

import asyncio
import os

from dotenv import load_dotenv

from trusttest.llm_clients import get_llm_client

load_dotenv(override=True)

client = get_llm_client(
    model="openai/gpt-oss-20b",
    provider="openai",
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://example.com/api/v1",
)

response = asyncio.run(
    client.complete(
        instructions="Tell me a fun fact about the moon in one sentence.",
    )
)

print(response)
