"""Example of automatic RAG test generation using Neo4j as knowledge base."""

import os

from dotenv import load_dotenv

from trusttest.evaluation_scenarios import EvaluationScenario
from trusttest.evaluator_suite import EvaluatorSuite
from trusttest.evaluators import CorrectnessEvaluator
from trusttest.knowledge_base.neo4j import Neo4jKnowledgeBase
from trusttest.probes.rag import RAGProbe
from trusttest.targets.testing import DummyTarget

load_dotenv(override=True)

url = os.getenv("NEO4J_URL")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")


knowledge_base = Neo4jKnowledgeBase(
    uri=url, username=username, password=password, language="English"
)

probe = RAGProbe(
    target=DummyTarget(),
    knowledge_base=knowledge_base,
    num_questions=2,
    language="English",
)
scenario = EvaluationScenario(
    name="Automatic RAG Test Generation (Neo4j)",
    description="Generate and evaluate RAG questions using Neo4j knowledge base.",
    evaluator_suite=EvaluatorSuite(
        evaluators=[CorrectnessEvaluator()],
        criteria="any_fail",
    ),
    category="functional",
    sub_category="question-answer",
)

test_set = probe.get_test_set()
results = scenario.evaluate(test_set)
results.display_summary()
