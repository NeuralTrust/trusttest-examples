"""Example of evaluating a local LLM (Ollama) with custom target implementation."""

import os

import ollama

from trusttest.dataset_builder import Dataset, DatasetItem
from trusttest.evaluation_contexts import ExpectedResponseContext
from trusttest.evaluation_scenarios import EvaluationScenario
from trusttest.evaluator_suite import EvaluatorSuite
from trusttest.evaluators import (
    CorrectnessEvaluator,
)
from trusttest.llm_clients import get_llm_client
from trusttest.probes import DatasetProbe
from trusttest.targets import Target

os.environ["OLLAMA_HOST"] = "http://localhost:11434"


class LocalLLMTarget(Target):
    """Local LLM model target."""

    def __init__(self):
        """Initialize the local LLM model target."""
        self.client = ollama.Client(host=os.getenv("OLLAMA_HOST"))

    async def async_respond(self, message: str) -> str:
        """Respond to a message."""
        res = self.client.chat(
            model="gemma3:1b", messages=[{"role": "user", "content": message}]
        )
        return res.message.content or ""


model_target = LocalLLMTarget()


dataset = Dataset(
    [
        [
            DatasetItem(
                question="What's the capital of Osona?",
                context=ExpectedResponseContext(
                    expected_response="The capital of Osona is Vic.",
                    question="What's the capital of Osona?",
                ),
            )
        ],
        [
            DatasetItem(
                question="What's the capital of Italy?",
                context=ExpectedResponseContext(
                    expected_response="The capital of Italy is Rome.",
                    question="What's the capital of Italy?",
                ),
            )
        ],
    ]
)

probe = DatasetProbe(target=model_target, dataset=dataset)
scenario = EvaluationScenario(
    description="Local LLM model scenario",
    name="Local LLM model scenario",
    evaluator_suite=EvaluatorSuite(
        evaluators=[
            CorrectnessEvaluator(
                llm_client=get_llm_client(provider="ollama", model="llama3.2")
            )
        ],
        criteria="any_fail",
    ),
)

test_set = probe.get_test_set()
results = scenario.evaluate(test_set)

results.display()
results.display_summary()
