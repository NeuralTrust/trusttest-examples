"""Example demonstrating how to update test set responses using BLEU evaluator."""

from trusttest.dataset_builder import Dataset, DatasetItem
from trusttest.evaluation_contexts import ExpectedResponseContext
from trusttest.evaluation_scenarios import EvaluationScenario
from trusttest.evaluator_suite import EvaluatorSuite
from trusttest.evaluators import BleuEvaluator
from trusttest.probes.dataset import DatasetProbe
from trusttest.targets.testing import DummyTarget

model = DummyTarget()
probe = DatasetProbe(
    target=model,
    dataset=Dataset(
        [
            [
                DatasetItem(
                    question="What is Python?",
                    context=ExpectedResponseContext(
                        expected_response="Python is a high-level, interpreted programming language.",
                        question="What is Python?",
                    ),
                )
            ]
        ]
    ),
)

test_set = probe.get_test_set()
scenario = EvaluationScenario(
    name="Quickstart Functional Test",
    description="Functional test example.",
    evaluator_suite=EvaluatorSuite(
        evaluators=[BleuEvaluator(threshold=0.3)],
        criteria="any_fail",
    ),
)

results = scenario.evaluate(test_set)
