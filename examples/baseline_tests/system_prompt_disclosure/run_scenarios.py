import os
from typing import List

from dotenv import load_dotenv

import trusttest
from trusttest.catalog.system_prompt_disclosure import (
    SystemPromptDisclosureScenarioBuilder,
)
from trusttest.language_detection.types import LanguageType
from trusttest.targets.http import HttpTarget, PayloadConfig

load_dotenv(override=True)


target = HttpTarget(
    url="https://example.com/api/chat",
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

languages: List[LanguageType] = ["English"]
sub_categories = SystemPromptDisclosureScenarioBuilder.sub_categories

for language in languages:
    builder = SystemPromptDisclosureScenarioBuilder(
        target=target,
        language=language,
        num_test_cases=1,
    )
    for sub_category in sub_categories:
        scenario = builder.get_scenario(sub_category)
        test_set = scenario.probe.get_test_set()

        results = scenario.eval.evaluate(test_set)
        results.display_summary()

        client.save_evaluation_scenario(scenario.eval)
        client.save_evaluation_scenario_test_set(scenario.eval.id, test_set)
        client.save_evaluation_scenario_run(results)
