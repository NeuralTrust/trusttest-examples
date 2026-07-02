import os

from dotenv import load_dotenv

import trusttest
from trusttest.catalog.sensitive_data_leak import run_scenarios
from trusttest.targets.http import HttpTarget, PayloadConfig

load_dotenv(override=True)


target = HttpTarget(
    url="https://my-chatbot/chat/banking",
    headers={
        "Content-Type": "application/json",
    },
    payload_config=PayloadConfig(
        rate_limit=1,
        timeout=60,
        format={
            "message": "{{ test }}",
        },
    ),
    concatenate_field="response",
)

client = trusttest.client(type="neuraltrust", token=os.getenv("CLIENT_TOKEN"))

run_scenarios(
    target=target,
    client=client,
    language="English",
    num_test_cases=1,
)
