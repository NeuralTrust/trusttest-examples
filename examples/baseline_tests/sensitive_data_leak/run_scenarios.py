import json
import os
from typing import List

from dotenv import load_dotenv

import trusttest
from trusttest.evaluation_scenarios import EvaluationScenario
from trusttest.evaluator_suite import EvaluatorSuite
from trusttest.evaluators import TrueFalseEvaluator
from trusttest.language_detection.types import LanguageType
from trusttest.probes.sensitive_data_leak import (
    ContextualLeakageRequestDatasetProbe,
    DirectQueryForSensitiveDataDatasetProbe,
    MisleadingContextRequestDatasetProbe,
    ObfuscatedDataRequestDatasetProbe,
)
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

probes = [
    (ContextualLeakageRequestDatasetProbe, "Contextual Leakage Request"),
    (DirectQueryForSensitiveDataDatasetProbe, "Direct Query for Sensitive Data"),
    (ObfuscatedDataRequestDatasetProbe, "Obfuscated Data Request"),
    (MisleadingContextRequestDatasetProbe, "Misleading Context Request"),
]
for ProbeClass, category_name in probes:
    for language in languages:
        probe = ProbeClass(
            target=target,
            translate_into_language=language,
            max_objectives_per_category=50,
        )
        test_set = probe.get_test_set()
        os.makedirs(
            f"datasets/{language}/sensitive_data_leak/{category_name}",
            exist_ok=True,
        )
        with open(
            f"datasets/{language}/sensitive_data_leak/{category_name}/test_set.json",
            "w",
        ) as f:
            json.dump(test_set.to_dict(), f, indent=2)

        scenario = EvaluationScenario(
            name=f"{category_name}",
            description=f"Test scenario for {category_name}",
            evaluator_suite=EvaluatorSuite(
                evaluators=[TrueFalseEvaluator()],
                criteria="any_fail",
            ),
            category="sensitive-data-leak",
        )
        results = scenario.evaluate(test_set)
        results.display_summary()

        client.save_evaluation_scenario(scenario)
        client.save_evaluation_scenario_test_set(scenario.id, test_set)
        client.save_evaluation_scenario_run(results)
