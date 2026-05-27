import os

from dotenv import load_dotenv

import trusttest
from trusttest.catalog.system_prompt_disclosure import run_scenarios
from trusttest.targets.http import HttpTarget, PayloadConfig

load_dotenv(override=True)


target = HttpTarget(
    url="https://example.com/chat",
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

client = trusttest.client(
    type="neuraltrust",
    token=os.getenv("CLIENT_TOKEN"),
    target_id=os.getenv("NEURALTRUST_TARGET_ID"),
)

run_scenarios(
    target=target,
    client=client,
    language="English",
    num_test_cases=1,
)
