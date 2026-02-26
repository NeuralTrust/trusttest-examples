"""Example testing competitor mentions using CompetitorsPromptProbe with custom instructions."""

from dotenv import load_dotenv

from trusttest.evaluation_scenarios import EvaluationScenario
from trusttest.evaluator_suite import EvaluatorSuite
from trusttest.evaluators import (
    TrueFalseEvaluator,
)
from trusttest.probes.off_topics import CompetitorsPromptProbe
from trusttest.targets.http import HttpTarget, PayloadConfig

load_dotenv(override=True)


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
        timeout=40,
    ),
    concatenate_field=".",
)


scenario = EvaluationScenario(
    description="This is a test scenario",
    name="Test Scenario",
    evaluator_suite=EvaluatorSuite(
        evaluators=[TrueFalseEvaluator()],
        criteria="any_fail",
    ),
)

probe = CompetitorsPromptProbe(
    target=model,
    instructions="Focus on asking about the competitors prices.",
    company="AirTrust",
    competitors=["Iberia", "Air Europa", "Vueling"],
    num_items=2,
)

test_set = probe.get_test_set()
results = scenario.evaluate(test_set)
results.display()
results.display_summary()
