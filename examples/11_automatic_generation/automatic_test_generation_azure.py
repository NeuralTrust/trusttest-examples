"""Example of automatic RAG test generation using Azure Search as knowledge base."""

import os

from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

from trusttest.catalog import RagFunctionalScenario
from trusttest.knowledge_base.azure_search import AzureKnowledgeBase
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

rag_test = RagFunctionalScenario(
    target=DummyTarget(),
    knowledge_base=knowledge_base,
    num_questions=2,
    language="French",
)

test_set = rag_test.probe.get_test_set()
results = rag_test.eval.evaluate(test_set)
results.display()
