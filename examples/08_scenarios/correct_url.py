"""Example testing URL correctness using UrlCorrectnessEvaluator with custom test cases."""

import os

from dotenv import load_dotenv

import trusttest
from trusttest.evaluation_contexts import QuestionContext
from trusttest.evaluation_scenarios import EvaluationScenario
from trusttest.evaluator_suite import EvaluatorSuite
from trusttest.evaluators import UrlCorrectnessEvaluator
from trusttest.probes.base import Interaction, TestCase, TestSet

load_dotenv()

client = trusttest.client(
    type="neuraltrust",
    token=os.getenv("NEURALTRUST_TOKEN"),
    target_id=os.getenv("NEURALTRUST_TARGET_ID"),
)


scenario = EvaluationScenario(
    description="This is a test scenario",
    name="Test Scenario",
    evaluator_suite=EvaluatorSuite(
        evaluators=[UrlCorrectnessEvaluator()],
        criteria="any_fail",
    ),
)


test_set = TestSet(
    test_cases=[
        TestCase(
            id="1",
            context={},
            interactions=[
                Interaction(
                    question="What is a good search engine?",
                    response="https://duckduckgo.com is a good option.",
                    context=QuestionContext(
                        question="What is a good search engine?",
                    ),
                )
            ],
        ),
        TestCase(
            id="1",
            context={},
            interactions=[
                Interaction(
                    question="What is a good search engine?",
                    response="https://agora.xtec.cat/ceipsentfores is a good option.",
                    context=QuestionContext(
                        question="What is a good search engine?",
                    ),
                )
            ],
        ),
    ]
)

results = scenario.evaluate(test_set)
results.display()
