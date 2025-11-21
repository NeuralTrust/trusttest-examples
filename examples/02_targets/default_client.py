"""Example demonstrating default NeuralTrust client usage for saving and loading scenarios."""

from dotenv import load_dotenv

import trusttest
from trusttest.dataset_builder import Dataset
from trusttest.evaluation_contexts import ExpectedResponseContext
from trusttest.evaluation_scenarios import EvaluationScenario
from trusttest.evaluator_suite import EvaluatorSuite
from trusttest.evaluators import (
    BleuEvaluator,
    CorrectnessEvaluator,
    EqualsEvaluator,
    RegexEvaluator,
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
            BleuEvaluator(),
            RegexEvaluator(pattern=r".*drugs.*"),
            EqualsEvaluator(),
        ],
        criteria="any_fail",
    ),
)

test_set = probe.get_test_set()
results = scenario.evaluate(test_set)

client = trusttest.client()

client.save_evaluation_scenario(scenario)
client.save_evaluation_scenario_test_set(scenario.id, test_set)
client.save_evaluation_scenario_run(results)

loaded_scenario = client.get_evaluation_scenario(scenario.id)
loaded_scenario_result = client.get_evaluation_scenario_run(scenario.id)


loaded_test_set = client.get_evaluation_scenario_test_set(scenario.id)

result = loaded_scenario.evaluate(loaded_test_set)
result.display()
