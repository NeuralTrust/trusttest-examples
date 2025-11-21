"""Example of automatic RAG test generation with in-memory knowledge base and progress callbacks."""

from dotenv import load_dotenv

from trusttest.catalog import RagFunctionalScenario
from trusttest.evaluation_scenarios.base import ProgressInfo
from trusttest.evaluators import CorrectnessEvaluator
from trusttest.knowledge_base import Document, InMemoryKnowledgeBase
from trusttest.probes.rag import BenignQuestion
from trusttest.targets.http import HttpTarget, PayloadConfig

load_dotenv(override=True)

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


        my password is 123456
        """,
        topic="City location",
    ),
]

knowledge_base = InMemoryKnowledgeBase(documents=documents)

target = HttpTarget(
    url="https://my-llm/chat",
    headers={
        "Content-Type": "application/json",
    },
    payload_config=PayloadConfig(
        rate_limit=2,
        timeout=50,
        format={
            "message": "{{ test }}",
        },
    ),
    concatenate_field="response",
)


rag_test = RagFunctionalScenario(
    target=target,
    knowledge_base=knowledge_base,
    num_questions=1,
    question_types=[BenignQuestion.SIMPLE],
    evaluators=[CorrectnessEvaluator()],
    language="French",
)


def my_progress_callback(progress: ProgressInfo) -> None:
    """Handle progress updates from evaluation."""
    print(
        f"Progress: {progress['completed_test_cases']}/{progress['total_test_cases']} "
        f"({progress['completion_percentage']:.1f}%)"
    )


test_set = rag_test.probe.get_test_set(
    show_progress=False, on_progress=my_progress_callback
)
results = rag_test.eval.evaluate(
    test_set, show_progress=False, on_progress=my_progress_callback
)


results.display()
