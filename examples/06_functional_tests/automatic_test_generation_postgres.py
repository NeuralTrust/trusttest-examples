"""Example of automatic RAG test generation using PostgreSQL with pgvector as knowledge base."""

import os

from dotenv import load_dotenv

from trusttest.evaluation_scenarios import EvaluationScenario
from trusttest.evaluator_suite import EvaluatorSuite
from trusttest.evaluators import CorrectnessEvaluator
from trusttest.knowledge_base.pgvector import PgVectorKnowledgeBase
from trusttest.probes.rag import BenignQuestion, RAGProbe
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

probe = RAGProbe(
    target=DummyTarget(),
    knowledge_base=kb,
    num_questions=2,
    question_types=[BenignQuestion.SIMPLE],
)
scenario = EvaluationScenario(
    name="Automatic RAG Test Generation (Postgres)",
    description="Generate and evaluate RAG questions using pgvector knowledge base.",
    evaluator_suite=EvaluatorSuite(
        evaluators=[CorrectnessEvaluator()],
        criteria="any_fail",
    ),
    category="functional",
    sub_category="question-answer",
)

test_set = probe.get_test_set()
results = scenario.evaluate(test_set)

results.display(samples=2)
