"""Baseline test for disallowed content using PoliticsDisallowedContentDatasetProbe with French translation."""

import os

from dotenv import load_dotenv

import trusttest
from trusttest.evaluation_scenarios import EvaluationScenario
from trusttest.evaluator_suite import EvaluatorSuite
from trusttest.evaluators import TrueFalseEvaluator
from trusttest.probes import PoliticsDisallowedContentDatasetProbe
from trusttest.targets.http import HttpTarget, PayloadConfig

load_dotenv(override=True)


client = trusttest.client(type="neuraltrust", token=os.getenv("NEURALTURST_TOKEN"))


target = HttpTarget(
    url="https://my-llm/chat_french",
    headers={
        "Content-Type": "application/json",
    },
    payload_config=PayloadConfig(
        rate_limit=1,
        timeout=60,
        format={
            "message": "{{ test }}",
        },
    ),
    concatenate_field="response",
)


probe = PoliticsDisallowedContentDatasetProbe(
    target=target, translate_into_language="French"
)
scenario = EvaluationScenario(
    name="Off Topic: Disallowed Content",
    description="Test scenario for disallowed content",
    evaluator_suite=EvaluatorSuite(
        evaluators=[TrueFalseEvaluator()],
        criteria="any_fail",
    ),
    category="off-topic",
    type="disallowed-content",
)

test_set = probe.get_test_set()
results = scenario.evaluate(test_set)
results.display_summary()

client.save_evaluation_scenario(scenario)
client.save_evaluation_scenario_test_set(scenario.id, test_set)
client.save_evaluation_scenario_run(results)
