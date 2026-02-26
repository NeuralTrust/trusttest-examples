"""Example of automatic RAG test generation using Azure Search as knowledge base."""

import os

from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

from trusttest.evaluation_scenarios import EvaluationScenario
from trusttest.evaluator_suite import EvaluatorSuite
from trusttest.evaluators import CorrectnessEvaluator
from trusttest.knowledge_base.azure_search import AzureKnowledgeBase
from trusttest.probes.rag import RAGProbe
from trusttest.targets.testing import DummyTarget

load_dotenv(override=True)

key = os.getenv("AZURE_SEARCH_KEY")

if not key:
    raise ValueError("AZURE_SEARCH_KEY is not set")

knowledge_base = AzureKnowledgeBase(
    credentials=AzureKeyCredential(key),
    service_endpoint=os.getenv("AZURE_SEARCH_SERVICE_ENDPOINT"),
    index_name=os.getenv("AZURE_SEARCH_INDEX_NAME"),
    fields_mapping={"content": "chunk", "id": "chunk_id"},
)

probe = RAGProbe(
    target=DummyTarget(),
    knowledge_base=knowledge_base,
    num_questions=2,
    language="French",
)
scenario = EvaluationScenario(
    name="Automatic RAG Test Generation (Azure)",
    description="Generate and evaluate RAG questions using Azure Search knowledge base.",
    evaluator_suite=EvaluatorSuite(
        evaluators=[CorrectnessEvaluator()],
        criteria="any_fail",
    ),
    category="functional",
    sub_category="question-answer",
    language="French",
)

test_set = probe.get_test_set()
results = scenario.evaluate(test_set)
results.display()
