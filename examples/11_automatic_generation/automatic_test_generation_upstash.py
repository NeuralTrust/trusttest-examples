"""Example of automatic RAG poisoning test generation using Upstash as knowledge base with custom config."""

import os

from dotenv import load_dotenv

import trusttest
from trusttest.catalog import RagPoisoningScenario
from trusttest.config import Config
from trusttest.knowledge_base.upstash import UpstashKnowledgeBase
from trusttest.probes.rag import MaliciousQuestion
from trusttest.targets.testing import DummyTarget

load_dotenv(override=True)

trusttest.set_config(
    Config(
        evaluator={
            "provider": "google",
            "model": "gemini-2.0-flash",
            "temperature": 0.2,
        },
        question_generator={
            "provider": "google",
            "model": "gemini-2.0-flash",
            "temperature": 0.5,
        },
        translation={
            "provider": "google",
            "model": "gemini-2.0-flash",
            "temperature": 0.2,
        },
        embeddings={"provider": "openai", "model": "text-embedding-3-small"},
        topic_summarizer={
            "provider": "google",
            "model": "gemini-2.0-flash",
            "temperature": 0.2,
        },
    )
)

url = os.getenv("UPSTASH_URL")
token = os.getenv("UPSTASH_TOKEN")

knowledge_base = UpstashKnowledgeBase(url=url, token=token)
knowledge_base.initialize_topics()

rag_test = RagPoisoningScenario(
    target=DummyTarget(),
    knowledge_base=knowledge_base,
    num_questions=2,
    question_types=[
        MaliciousQuestion.SPECIAL_TOKEN,
    ],
    language="Catalan",
)

test_set = rag_test.probe.get_test_set()
results = rag_test.eval.evaluate(test_set)
results.display()
results.display_summary()
