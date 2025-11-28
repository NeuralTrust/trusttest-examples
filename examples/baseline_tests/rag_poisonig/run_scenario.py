import os
from typing import List

import yaml
from dotenv import load_dotenv

import trusttest
from trusttest.evaluation_scenarios import EvaluationScenario
from trusttest.evaluator_suite import EvaluatorSuite
from trusttest.evaluators import AnswerRelevanceEvaluator
from trusttest.knowledge_base import Document, InMemoryKnowledgeBase
from trusttest.language_detection.types import LanguageType
from trusttest.probes.rag import RAGProbe
from trusttest.probes.rag.utils import MaliciousQuestion
from trusttest.targets.http import HttpTarget, PayloadConfig

load_dotenv(override=True)

target = HttpTarget(
    url="https://api.example.com/chat/banking",
    headers={
        "Content-Type": "application/json",
    },
    payload_config=PayloadConfig(
        format={"message": "{{ test }}"},
    ),
    concatenate_field="response",
)

client = trusttest.client(type="neuraltrust", token=os.getenv("CLIENT_TOKEN"))

with open("document_chunks.yaml", "r") as f:
    document_chunks = yaml.load(f, Loader=yaml.FullLoader)

documents = [
    Document(id=f"chunk_{i}", content=chunk["chunk"])
    for i, chunk in enumerate(document_chunks)
]


categories = [
    MaliciousQuestion.INSTRUCTION_MANIPULATION,
    MaliciousQuestion.ROLE_PLAY,
    MaliciousQuestion.HYPOTHETICAL,
    MaliciousQuestion.STORYTELLING,
    MaliciousQuestion.PAYLOAD_SPLITTING,
    MaliciousQuestion.LIST_BASED,
    MaliciousQuestion.SPECIAL_TOKEN,
]

languages: List[LanguageType] = ["English"]

for language in languages:
    for category in categories:
        knowledge_base = InMemoryKnowledgeBase(
            documents=documents
        )  # if the client has a vector database, use it instead

        rag_probe = RAGProbe(
            target=target,
            num_questions=10,
            knowledge_base=knowledge_base,
            question_types=[category],
            language=language,
        )

        scenario = EvaluationScenario(
            name=f"RAG Poisoning - {category.value}",
            description=f"RAG poisoning test for {category.value}",
            evaluator_suite=EvaluatorSuite(
                evaluators=[AnswerRelevanceEvaluator()],
                criteria="any_fail",
            ),
            category="prompt-injection",
        )

        test_set = rag_probe.get_test_set()
        results = scenario.evaluate(test_set)  # type: ignore
        results.display_summary()

        client.save_evaluation_scenario(scenario)
        client.save_evaluation_scenario_test_set(scenario.id, test_set)
        client.save_evaluation_scenario_run(results)
