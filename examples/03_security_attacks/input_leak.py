"""Example testing input persistence and leakage using InputPersistenceCheckDatasetProbe."""

import os

from dotenv import load_dotenv

from trusttest.evaluation_scenarios import EvaluationScenario
from trusttest.evaluator_suite import EvaluatorSuite
from trusttest.evaluators import TrueFalseEvaluator
from trusttest.probes import InputPersistenceCheckDatasetProbe
from trusttest.targets.http import HttpTarget, PayloadConfig

load_dotenv(override=True)

target = HttpTarget(
    url="https://example.com/api/chat",
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
    },
    payload_config=PayloadConfig(
        format={
            "model": "o4-mini-2025-04-16",
            "messages": [
                {
                    "role": "user",
                    "content": "{{ test }}",
                }
            ],
        },
        message_regex="{{ test }}",
        timeout=60,
    ),
    concatenate_field="choices.0.message.content",
)

probe = InputPersistenceCheckDatasetProbe(
    target=target,
    max_objectives_per_category=1,
)

scenario = EvaluationScenario(
    description="This is a test scenario",
    name="Test Scenario",
    evaluator_suite=EvaluatorSuite(
        evaluators=[TrueFalseEvaluator()],
        criteria="any_fail",
    ),
)

test_set = probe.get_test_set()
results = scenario.evaluate(test_set)
results.display()
results.display_summary()
