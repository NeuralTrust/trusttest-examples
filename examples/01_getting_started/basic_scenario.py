"""Basic scenario example with dataset probe, correctness and BLEU evaluators."""

from dotenv import load_dotenv

from trusttest.dataset_builder import Dataset
from trusttest.evaluation_contexts import ExpectedResponseContext
from trusttest.evaluation_scenarios import EvaluationScenario
from trusttest.evaluator_suite import EvaluatorSuite
from trusttest.evaluators import (
    BleuEvaluator,
    CorrectnessEvaluator,
)
from trusttest.probes import DatasetProbe
from trusttest.targets.testing import DummyTarget

load_dotenv()

dataset_path = "examples/data/qa_dataset.json"
dataset: Dataset[ExpectedResponseContext] = Dataset.from_json(path=dataset_path)
probe = DatasetProbe(target=DummyTarget(), dataset=dataset)


scenario = EvaluationScenario(
    description="This is a test scenario",
    name="Test Scenario",
    evaluator_suite=EvaluatorSuite(
        evaluators=[
            CorrectnessEvaluator(),
            BleuEvaluator(n_grams=1, smoothing_method="method1"),
        ],
        criteria="any_fail",
    ),
)

test_set = probe.get_test_set()
results = scenario.evaluate(test_set)
results.display()
