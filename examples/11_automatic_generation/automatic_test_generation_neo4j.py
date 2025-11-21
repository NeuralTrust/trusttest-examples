"""Example of automatic RAG test generation using Neo4j as knowledge base."""

import os

from dotenv import load_dotenv

from trusttest.catalog import RagFunctionalScenario
from trusttest.knowledge_base.neo4j import Neo4jKnowledgeBase
from trusttest.targets.testing import DummyTarget

load_dotenv(override=True)

url = os.getenv("NEO4J_URL")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")


knowledge_base = Neo4jKnowledgeBase(
    uri=url, username=username, password=password, language="English"
)

rag_test = RagFunctionalScenario(
    target=DummyTarget(), knowledge_base=knowledge_base, num_questions=2
)

test_set = rag_test.probe.get_test_set()
results = rag_test.eval.evaluate(test_set)
results.display_summary()
