import json
import os
from typing import List

from dotenv import load_dotenv

import trusttest
from trusttest.evaluation_scenarios import EvaluationScenario
from trusttest.evaluator_suite import EvaluatorSuite
from trusttest.evaluators import TrueFalseEvaluator
from trusttest.language_detection.types import LanguageType
from trusttest.probes import CompetitorsDatasetProbe
from trusttest.targets.http import HttpTarget, PayloadConfig

load_dotenv(override=True)


target = HttpTarget(
    url="https://api.example.com/chat/banking",
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
for language in languages:
    probe = CompetitorsDatasetProbe(
        target=target,
        company="ExampleCompany",  # Define the client company
        competitors=["OpenAI", "Anthropic", "Cohere", "Google", "Microsoft", "Meta"],
        translate_into_language=language,
        max_objectives_per_category=50,
    )

    test_set = probe.get_test_set()
    with open(f"datasets/{language}/competitors_check/test_set.json", "w") as f:
        json.dump(test_set.to_dict(), f, indent=2)

    scenario = EvaluationScenario(
        name="Competitors Check",
        description="Test scenario for competitors check",
        evaluator_suite=EvaluatorSuite(
            evaluators=[TrueFalseEvaluator()],
            criteria="any_fail",
        ),
        category="off-topic",
    )
    results = scenario.evaluate(test_set)
    results.display_summary()

    client.save_evaluation_scenario(scenario)
    client.save_evaluation_scenario_test_set(scenario.id, test_set)
    client.save_evaluation_scenario_run(results)
