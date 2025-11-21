"""Example of automatic RAG test generation using PostgreSQL with pgvector as knowledge base."""

import os

from dotenv import load_dotenv

from trusttest.catalog.rag import BenignQuestion, RagFunctionalScenario
from trusttest.knowledge_base.pgvector import PgVectorKnowledgeBase
from trusttest.targets.testing import DummyTarget

load_dotenv()

kb = PgVectorKnowledgeBase(
    connection_string=os.getenv(
        "POSTGRES_CONNECTION_STRING",
        "postgresql://postgres:postgres@localhost:5432/postgres",
    ),
    table_name="my_vectors",
    fields_mapping={
        "id": "uuid",
        "content": "document",
        "embeddings": "embedding",
    },
)

rag_test = RagFunctionalScenario(
    target=DummyTarget(),
    knowledge_base=kb,
    num_questions=2,
    question_types=[BenignQuestion.SIMPLE],
)

test_set = rag_test.probe.get_test_set()
results = rag_test.eval.evaluate(test_set)

results.display(samples=2)
