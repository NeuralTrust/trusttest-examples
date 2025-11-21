"""Example demonstrating DeepSeek API usage with get_llm_client."""

import asyncio
import os

from trusttest.llm_clients import get_llm_client

os.environ["DEEPSEEK_BASE_URL"] = "https://api.deepseek.com"
os.environ["DEEPSEEK_API_KEY"] = "<your-api-key>"

llm = get_llm_client(model="deepseek-chat", provider="deepseek")

response = asyncio.run(llm.complete("Return a json saying hello"))
print(response)
