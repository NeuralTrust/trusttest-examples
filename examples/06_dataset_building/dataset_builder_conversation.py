"""Example using ConversationDatasetBuilder with ExpectedResponseContext for multi-turn country capital questions."""

from dotenv import load_dotenv

from trusttest.dataset_builder import ConversationDatasetBuilder, DatasetItem
from trusttest.evaluation_contexts import ExpectedResponseContext

load_dotenv()


builder = ConversationDatasetBuilder(
    instructions="""
    Build a dataset for country capital questions.
    """,
    context_type=ExpectedResponseContext,
    examples=[
        DatasetItem(
            question="What is the capital of France?",
            context=ExpectedResponseContext(
                expected_response="Paris",
                question="What is the capital of France?",
            ),
        ),
    ],
    language="English",
    num_items=10,
    max_messages=3,
)

result = builder.build()

for item in result.items:
    for message in item:
        print(message.question)
        print(message.context)
        print("-" * 100)
    print("=" * 100)
