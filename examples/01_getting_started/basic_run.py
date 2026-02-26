"""Basic example of running evaluation with HTTP target, dataset probe, and saving results to NeuralTrust."""

import os

from dotenv import load_dotenv

import trusttest
from trusttest.dataset_builder import Dataset
from trusttest.evaluation_contexts import ExpectedResponseContext
from trusttest.evaluation_scenarios import EvaluationScenario
from trusttest.evaluator_suite import EvaluatorSuite
from trusttest.evaluators import CorrectnessEvaluator
from trusttest.probes import DatasetProbe
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

dataset: Dataset[ExpectedResponseContext] = Dataset.from_json(
    path="examples/data/qa_dataset.json"
)
probe = DatasetProbe(target=target, dataset=dataset)

scenario: EvaluationScenario[ExpectedResponseContext] = EvaluationScenario(
    description="This is a test scenario",
    name="Hola",
    evaluator_suite=EvaluatorSuite(
        evaluators=[CorrectnessEvaluator()],
        criteria="any_fail",
    ),
)

test_set = probe.get_test_set()
results = scenario.evaluate(test_set)

results.display_summary()


client = trusttest.client(
    type="neuraltrust",
    token=os.getenv("MY_NEURALTRUST_TOKEN"),
    verify=False,
)

client.save_evaluation_scenario(scenario)
client.save_evaluation_scenario_test_set(scenario.id, test_set)
client.save_evaluation_scenario_run(results)
