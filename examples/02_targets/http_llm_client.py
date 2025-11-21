"""Example demonstrating HTTPClient usage for custom LLM API endpoints with retry configuration."""

import asyncio
import os

from dotenv import load_dotenv

from trusttest.llm_clients import HTTPClient, RetryConfig

load_dotenv()

http_client = HTTPClient(
    url="https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent",
    headers={
        "Content-Type": "application/json",
        "X-goog-api-key": os.getenv("GOOGLE_API_KEY") or "",
    },
    payload_config={
        "contents": [
            {"role": "model", "parts": [{"text": "{{ system_prompt }}"}]},
            {"role": "user", "parts": [{"text": "{{ instructions }}"}]},
        ],
        "generationConfig": {"responseMimeType": "application/json"},
    },
    concatenate_field="candidates.0.content.parts.0.text",
    retry_config=RetryConfig(
        attempts=3,
        initial_delay=1.0,
        max_delay=10.0,
        exp_base=2.0,
    ),
)


response = asyncio.run(
    http_client.complete(
        instructions="Hello, how are you?",
        system_prompt="Return a json with key response.",
    )
)
print(response)
