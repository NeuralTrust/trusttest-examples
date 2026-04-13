"""Example using ConversationDatasetBuilder with ObjectiveContext for multi-turn conversations."""

from dotenv import load_dotenv

from trusttest.dataset_builder import ConversationDatasetBuilder
from trusttest.evaluation_contexts import ObjectiveContext

load_dotenv()


builder = ConversationDatasetBuilder(
    instructions="""
    questions about customer support airline.
    """,
    examples=[],
    language="English",
    num_items=2,
    max_messages=3,
    context_type=ObjectiveContext,
)

result = builder.build()

print(builder.system_prompt)

for item in result.items:
    for message in item:
        print(message.question)
        print(message.context)
        print("-" * 100)
    print("=" * 100)
