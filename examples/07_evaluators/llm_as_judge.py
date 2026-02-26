"""Example demonstrating LLM-as-judge evaluation using custom OpenAiClient for CorrectnessEvaluator."""

from dotenv import load_dotenv

from trusttest.dataset_builder import Dataset, DatasetItem
from trusttest.evaluation_contexts import ExpectedResponseContext
from trusttest.evaluation_scenarios import EvaluationScenario
from trusttest.evaluator_suite import EvaluatorSuite
from trusttest.evaluators import (
    CorrectnessEvaluator,
)
from trusttest.llm_clients.openai_client import OpenAiClient
from trusttest.probes.dataset import DatasetProbe
from trusttest.targets.testing import DummyTarget

load_dotenv()

llm_client = OpenAiClient(
    model="gpt-4o-mini",
    temperature=0.2,
)

evaluator = CorrectnessEvaluator(llm_client=llm_client)

scenario = EvaluationScenario(
    name="Functional Test",
    description="Functional test example.",
    evaluator_suite=EvaluatorSuite(
        evaluators=[evaluator],
        criteria="any_fail",
    ),
)

probe = DatasetProbe(
    target=DummyTarget(),
    dataset=Dataset(
        [
            [
                DatasetItem(
                    question="What is Python?",
                    context=ExpectedResponseContext(
                        expected_response="Python is a high-level, interpreted programming language.",
                        question="What is Python?",
                    ),
                )
            ]
        ]
    ),
)

test_set = probe.get_test_set()

results = scenario.evaluate(test_set)
results.display_summary()
