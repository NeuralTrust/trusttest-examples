"""Example using SinglePromptDatasetBuilder with ExpectedResponseContext for customer support questions."""

from dotenv import load_dotenv

from trusttest.dataset_builder import SinglePromptDatasetBuilder
from trusttest.evaluation_contexts import ExpectedResponseContext

load_dotenv(override=True)


builder = SinglePromptDatasetBuilder(
    instructions="""
    questions about customer support airline.
    """,
    context_type=ExpectedResponseContext,
    examples=[],
    language="English",
    num_items=20,
)

result = builder.build()
