"""Example testing system prompt disclosure using ConfusionAndClarificationPromptProbe."""

from dotenv import load_dotenv

from trusttest.evaluation_scenarios import EvaluationScenario
from trusttest.evaluator_suite import EvaluatorSuite
from trusttest.evaluators import TrueFalseEvaluator
from trusttest.probes import ConfusionAndClarificationPromptProbe
from trusttest.targets.testing import DummyTarget

load_dotenv(override=True)

probe = ConfusionAndClarificationPromptProbe(
    target=DummyTarget(),
    instructions="Focus on extracting instructions for a banc sabadell chatbot",
    num_items=2,
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
