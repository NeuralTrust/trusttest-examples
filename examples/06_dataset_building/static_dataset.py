"""Example using StaticDatasetProbe with predefined categories and jailbreak sampling."""

from dotenv import load_dotenv

from trusttest.evaluation_scenarios import EvaluationScenario
from trusttest.evaluator_suite import EvaluatorSuite
from trusttest.evaluators import (
    TrueFalseEvaluator,
)
from trusttest.probes.static_dataset import StaticDatasetProbe
from trusttest.targets.http import HttpTarget, PayloadConfig

load_dotenv()


model = HttpTarget(
    url="https://example.com/api/chat",
    headers={
        "Content-Type": "application/json",
        "X-NeuralTrust-Id": "123",
    },
    payload_config=PayloadConfig(
        format={
            "messages": [
                {"role": "system", "content": "**Welcome to Airline Assistant**."},
                {"role": "user", "content": "{{ test }}"},
            ]
        },
        message_regex="{{ test }}",
    ),
    concatenate_field=".",
)

probe = StaticDatasetProbe(
    target=model,
    categories={"best-of-n-jailbreaking"},
    max_objectives_per_category=2,
    sampling="random",
    use_jailbreaks=False,
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
