"""Example testing competitor mentions using CompetitorsDatasetProbe with translation support."""

from dotenv import load_dotenv

from trusttest.evaluation_scenarios import EvaluationScenario
from trusttest.evaluator_suite import EvaluatorSuite
from trusttest.evaluators import (
    TrueFalseEvaluator,
)
from trusttest.probes.off_topics import CompetitorsDatasetProbe
from trusttest.targets.http import HttpTarget, PayloadConfig

load_dotenv(override=True)


target = HttpTarget(
    url="https://example.com/api/chat",
    headers={
        "Content-Type": "application/json",
    },
    payload_config=PayloadConfig(
        format={"message": "{{ test }}"},
    ),
    concatenate_field="response",
)

scenario = EvaluationScenario(
    description="This is a test scenario",
    name="Test Scenario",
    evaluator_suite=EvaluatorSuite(
        evaluators=[TrueFalseEvaluator()],
        criteria="any_fail",
    ),
)

probe = CompetitorsDatasetProbe(
    target=target,
    max_objectives_per_category=5,
    company="AirTrust",
    competitors=["Iberia", "Air Europa", "Vueling"],
    translate_into_language="Spanish",
)

test_set = probe.get_test_set()
results = scenario.evaluate(test_set)
results.display()
results.display_summary()
