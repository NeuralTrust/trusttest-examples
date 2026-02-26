"""Example of automatic RAG poisoning test generation using Upstash as knowledge base with custom config."""

import os

from dotenv import load_dotenv

import trusttest
from trusttest.config import Config
from trusttest.evaluation_scenarios import EvaluationScenario
from trusttest.evaluator_suite import EvaluatorSuite
from trusttest.evaluators import CorrectnessEvaluator
from trusttest.knowledge_base.upstash import UpstashKnowledgeBase
from trusttest.probes.rag import MaliciousQuestion, RAGProbe
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

probe = RAGProbe(
    target=DummyTarget(),
    knowledge_base=knowledge_base,
    num_questions=2,
    question_types=[
        MaliciousQuestion.SPECIAL_TOKEN,
    ],
    language="Catalan",
)
scenario = EvaluationScenario(
    name="Automatic RAG Poisoning Test Generation (Upstash)",
    description="Generate and evaluate malicious RAG prompts using Upstash knowledge base.",
    evaluator_suite=EvaluatorSuite(
        evaluators=[CorrectnessEvaluator()],
        criteria="any_fail",
    ),
    category="security",
    sub_category="rag-poisoning",
    language="Catalan",
)

test_set = probe.get_test_set()
results = scenario.evaluate(test_set)
results.display()
results.display_summary()
