"""Example demonstrating custom LLM configuration for RAG scenarios with different providers and models."""

from dotenv import load_dotenv

import trusttest
from trusttest.catalog import RagFunctionalScenario
from trusttest.config import Config, EmbeddingsConfig, LLMConfig
from trusttest.evaluators import CorrectnessEvaluator
from trusttest.knowledge_base import Document, InMemoryKnowledgeBase
from trusttest.probes.rag import BenignQuestion
from trusttest.targets.testing import IcantAssistTarget

load_dotenv(override=True)


trusttest.set_config(
    Config(
        question_generator=LLMConfig(
            provider="google",
            model="gemini-2.0-flash",
            temperature=0.5,
        ),
        evaluator=LLMConfig(
            provider="openai",
            model="gpt-4o-mini",
            temperature=0.1,
        ),
        embeddings=EmbeddingsConfig(
            provider="openai",
            model="text-embedding-3-small",
        ),
        topic_summarizer=LLMConfig(
            provider="openai",
            model="gpt-4o-mini",
            temperature=0.1,
        ),
    )
)
documents = [
    Document(
        id="1",
        content="""
        Vic is of ancient origin. In past times it was called Ausa by the Romans.
        Iberian coins bearing this name have been found there.
        The Visigoths called it Ausona.
        Sewage caps on sidewalks around the city will also read "Vich", an old spelling of the name.
        """,
        topic="City origins",
    ),
    Document(
        id="2",
        content="""
        Vic (Catalan pronunciation: [bik]; Spanish: Vic) is the capital of the comarca of Osona,
        in the province of Barcelona, Catalonia, Spain.
        Vic is located 69 km (43 mi) from Barcelona and 60 km (37 mi) from Girona.
        """,
        topic="City location",
    ),
]

knowledge_base = InMemoryKnowledgeBase(documents=documents, language="Catalan")

model = IcantAssistTarget()

rag_test = RagFunctionalScenario(
    target=model,
    knowledge_base=knowledge_base,
    num_questions=2,
    question_types=[BenignQuestion.SIMPLE],
    evaluators=[CorrectnessEvaluator()],
)

test_set = rag_test.probe.get_test_set()
results = rag_test.eval.evaluate(test_set)
results.display()
