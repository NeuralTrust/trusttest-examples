import os

import yaml
from dotenv import load_dotenv

import trusttest
from trusttest.evaluation_scenarios import EvaluationScenario
from trusttest.evaluator_suite import EvaluatorSuite
from trusttest.evaluators import AnswerRelevanceEvaluator
from trusttest.knowledge_base import Document, InMemoryKnowledgeBase
from trusttest.probes.rag import RAGProbe
from trusttest.probes.rag.utils import BenignQuestion
from trusttest.targets.http import HttpTarget, PayloadConfig

load_dotenv(override=True)

target = HttpTarget(
    url="https://example.com/chat",
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
    document_chunks = yaml.safe_load(f)

documents = [
    Document(id=f"chunk_{i}", content=chunk["chunk"], topic="knowledge_base")
    for i, chunk in enumerate(document_chunks)
]
knowledge_base = InMemoryKnowledgeBase(
    documents=documents
)  # if the client has a vector database, use it instead

rag_probe = RAGProbe(
    target=target,
    num_questions=10,
    knowledge_base=knowledge_base,
    question_types=[BenignQuestion.SIMPLE],
)

frameworks = {
    "EU AI Act": "Art. 15 Accuracy, Robustness & Cybersecurity",
    "OWASP AITG": "AITG-APP-11 Hallucinations",
    "MITRE ATLAS": "AML.T0062 Hallucination",
    "OWASP LLM TOP10": "LLM09 Misinformation",
    "ISO/IEC 42001 (cl.)": "8.2 Operational planning and control",
}
scenario = EvaluationScenario(
    name="Functional Test",
    description="Functional test example.",
    evaluator_suite=EvaluatorSuite(
        evaluators=[AnswerRelevanceEvaluator()],
        criteria="any_fail",
    ),
    category="functional",
    sub_category="question-answer",
    language="English",
    frameworks=frameworks,
)

test_set = rag_probe.get_test_set()
results = scenario.evaluate(test_set)  # type: ignore
results.display_summary()

client.save_evaluation_scenario(scenario)
client.save_evaluation_scenario_test_set(scenario.id, test_set)
client.save_evaluation_scenario_run(results)
