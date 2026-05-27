"""Example of evaluating an HTTP endpoint with custom payload configuration and system messages."""

import os

from dotenv import load_dotenv

import trusttest
from trusttest.dataset_builder import Dataset
from trusttest.evaluation_contexts import ExpectedResponseContext
from trusttest.evaluation_scenarios import EvaluationScenario
from trusttest.evaluator_suite import EvaluatorSuite
from trusttest.evaluators import (
    CompletenessEvaluator,
    CorrectnessEvaluator,
    ToneEvaluator,
)
from trusttest.probes import DatasetProbe
from trusttest.targets.http import HttpTarget, PayloadConfig

load_dotenv(override=True)

client = trusttest.client(
    type="neuraltrust",
    token=os.getenv("NEURALTRUST_TOKEN"),
    target_id=os.getenv("NEURALTRUST_TARGET_ID"),
)


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
        }
    ),
)

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

dataset_path = "examples/data/qa_dataset.json"
dataset: Dataset[ExpectedResponseContext] = Dataset.from_json(path=dataset_path)
test_set = DatasetProbe(target=model, dataset=dataset).get_test_set()
results = scenario.evaluate(test_set)
results.display()


# client.save_evaluation_scenario(scenario)
# client.save_evaluation_scenario_test_set(scenario.id, test_set)
# client.save_evaluation_scenario_run(results)
