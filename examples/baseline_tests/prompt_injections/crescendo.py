import json
import os
from pathlib import Path
from typing import List

from dotenv import load_dotenv

import trusttest
from trusttest.evaluation_scenarios import EvaluationScenario
from trusttest.evaluator_suite import EvaluatorSuite
from trusttest.evaluators import TrueFalseEvaluator
from trusttest.language_detection.types import LanguageType
from trusttest.probes import Objective
from trusttest.probes.prompt_injections import CrescendoAttackProbe
from trusttest.targets.http import HttpTarget, PayloadConfig

load_dotenv(override=True)


target = HttpTarget(
    url="https://api.example.com/chat/banking_french",
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

objectives_data = json.load(open(Path(".") / "default-malicious-objectives.json"))
objectives = [
    Objective(
        question=objective["objective"],
        true_description=objective["true_description"],
        false_description=objective["false_description"],
    )
    for objective in objectives_data
]

client = trusttest.client(type="neuraltrust", token=os.getenv("CLIENT_TOKEN"))

languages: List[LanguageType] = ["English"]
for language in languages:
    os.makedirs(f"datasets/{language}/crescendo", exist_ok=True)
    probe = CrescendoAttackProbe(
        target=target, objectives=objectives, max_turns=1, language=language
    )
    test_set = probe.get_test_set()

    with open(f"datasets/{language}/crescendo/test_set.json", "w") as f:
        json.dump(test_set.to_dict(), f, indent=2)

    scenario = EvaluationScenario(
        name="Crescendo Attack",
        description="Test scenario for crescendo attack",
        evaluator_suite=EvaluatorSuite(
            evaluators=[TrueFalseEvaluator()],
            criteria="any_fail",
        ),
        category="prompt-injections",
    )

    results = scenario.evaluate(test_set)
    results.display_summary()

    client.save_evaluation_scenario(scenario)
    client.save_evaluation_scenario_test_set(scenario.id, test_set)
    client.save_evaluation_scenario_run(results)
