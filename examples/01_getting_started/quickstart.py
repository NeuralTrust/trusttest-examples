"""Quickstart example demonstrating basic evaluation scenario setup with dataset probe and evaluators."""

import os

import trusttest
from trusttest.dataset_builder import Dataset, DatasetItem
from trusttest.evaluation_contexts import ExpectedResponseContext
from trusttest.evaluation_scenarios import EvaluationScenario
from trusttest.evaluator_suite import EvaluatorSuite
from trusttest.evaluators import (
    CompletenessEvaluator,
    CorrectnessEvaluator,
    ToneEvaluator,
)
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
            ],
            [
                DatasetItem(
                    question="What is the capital of France?",
                    context=ExpectedResponseContext(
                        expected_response="The capital of France is Paris.",
                        question="What is the capital of France?",
                    ),
                )
            ],
        ]
    ),
)

test_set = probe.get_test_set()


scenario = EvaluationScenario(
    name="Functional Test",
    description="Functional test example.",
    evaluator_suite=EvaluatorSuite(
        evaluators=[
            CorrectnessEvaluator(),
            ToneEvaluator(),
            CompletenessEvaluator(),
        ],
        criteria="any_fail",
    ),
)


results = scenario.evaluate(test_set)
results.display()
results.display_summary()

results = scenario.evaluate(test_set)
results.display()
results.display_summary()


client = trusttest.client(type="neuraltrust", token=os.getenv("NEURALTRUST_TOKEN"))

client.save_evaluation_scenario(scenario)
client.save_evaluation_scenario_test_set(scenario.id, test_set)
client.save_evaluation_scenario_run(results)
