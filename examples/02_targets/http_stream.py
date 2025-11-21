"""Example demonstrating HTTP streaming responses with HttpTarget using stream=True."""

import os

from dotenv import load_dotenv

from trusttest.targets.http import HttpTarget, PayloadConfig

load_dotenv()

model = HttpTarget(
    url="https://api.openai.com/v1/chat/completions",
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
    },
    payload_config=PayloadConfig(
        format={
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "user",
                    "content": "{{ test }}",
                }
            ],
            "stream": True,
        },
        message_regex="{{ test }}",
    ),
    concatenate_field="choices.0.delta.content",
)


response = model.respond("Hello, how are you?")
print(response)
