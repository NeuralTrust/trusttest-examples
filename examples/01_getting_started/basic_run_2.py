"""Basic example using DummyTarget with dataset probe and correctness evaluator."""

from dotenv import load_dotenv

from trusttest.dataset_builder import Dataset
from trusttest.evaluation_contexts import ExpectedResponseContext
from trusttest.evaluation_scenarios import EvaluationScenario
from trusttest.evaluator_suite import EvaluatorSuite
from trusttest.evaluators import CorrectnessEvaluator
from trusttest.probes import DatasetProbe
from trusttest.targets.testing import DummyTarget

load_dotenv(override=True)


dataset_path = "examples/data/qa_dataset.json"
dataset: Dataset[ExpectedResponseContext] = Dataset.from_json(path=dataset_path)
probe = DatasetProbe(target=DummyTarget(), dataset=dataset)

scenario: EvaluationScenario[ExpectedResponseContext] = EvaluationScenario(
    description="This is a test scenario",
    name="Test Scenario",
    evaluator_suite=EvaluatorSuite(
        evaluators=[CorrectnessEvaluator()],
        criteria="any_fail",
    ),
)

test_set = probe.get_test_set()
results = scenario.evaluate(test_set)

results.display()
results.display_summary()
