"""Example using DatasetProbe with SinglePromptDatasetBuilder to evaluate a dataset."""

from dotenv import load_dotenv

from trusttest.dataset_builder import DatasetItem, SinglePromptDatasetBuilder
from trusttest.evaluation_contexts import ExpectedResponseContext
from trusttest.evaluation_scenarios import EvaluationScenario
from trusttest.evaluator_suite import EvaluatorSuite
from trusttest.evaluators import CorrectnessEvaluator
from trusttest.probes.dataset import DatasetProbe
from trusttest.targets.http import HttpTarget, PayloadConfig

load_dotenv(override=True)


dataset_builder = SinglePromptDatasetBuilder(
    instructions="""
    Build a dataset for country capital questions.
    """,
    examples=[
        DatasetItem(
            question="What is the capital of France?",
            context=ExpectedResponseContext(
                expected_response="Paris",
                question="What is the capital of France?",
            ),
        ),
    ],
    context_type=ExpectedResponseContext,
    language="English",
    num_items=2,
)

dataset = dataset_builder.build()

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
    ),
    concatenate_field=".",
)

probe = DatasetProbe(
    target=model,
    dataset=dataset,
)
scenario = EvaluationScenario(
    name="QA Scenario",
    description="Evaluate generated QA dataset with correctness checks.",
    evaluator_suite=EvaluatorSuite(
        evaluators=[CorrectnessEvaluator()],
        criteria="any_fail",
    ),
)


test_set = probe.get_test_set()
results = scenario.evaluate(test_set)
results.display()
