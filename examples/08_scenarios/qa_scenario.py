"""Example using DatasetScenario with SinglePromptDatasetBuilder to build and evaluate a dataset."""

from dotenv import load_dotenv

from trusttest.catalog import DatasetScenario
from trusttest.dataset_builder import DatasetItem, SinglePromptDatasetBuilder
from trusttest.evaluation_contexts import ExpectedResponseContext
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
    language="english",
    num_items=2,
)

dataset = dataset_builder.build()

model = HttpTarget(
    url="https://chat.neuraltrust.ai/api/chat",
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

scenario = DatasetScenario(
    target=model,
    dataset=dataset,
)


test_set = scenario.probe.get_test_set()
results = scenario.eval.evaluate(test_set)
results.display()
