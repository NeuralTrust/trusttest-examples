"""Baseline test for competitor mentions using CompetitorsDatasetProbe with French translation."""

import os

from dotenv import load_dotenv

import trusttest
from trusttest.evaluation_scenarios import EvaluationScenario
from trusttest.evaluator_suite import EvaluatorSuite
from trusttest.evaluators import TrueFalseEvaluator
from trusttest.probes import CompetitorsDatasetProbe
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


probe = CompetitorsDatasetProbe(
    target=target,
    company="Credit Agricole",
    competitors=[
        "Santander",
        "BNP Paribas",
        "Société Générale",
        "La Banque Postale",
        "Crédit Mutuel",
        "CIC",
        "Banque Populaire",
        "Caisse d'Epargne",
        "LCL",
        "HSBC France",
        "Boursorama Banque",
        "AXA Banque",
        "Monabanq",
        "Hello bank!",
        "ING France",
    ],
    translate_into_language="French",
)
scenario = EvaluationScenario(
    name="Off Topic: Competitors Check",
    description="Test scenario for competitors",
    evaluator_suite=EvaluatorSuite(
        evaluators=[TrueFalseEvaluator()],
        criteria="any_fail",
    ),
    category="off-topic",
    type="competitors-check",
)

test_set = probe.get_test_set()
results = scenario.evaluate(test_set)
results.display_summary()

client.save_evaluation_scenario(scenario)
client.save_evaluation_scenario_test_set(scenario.id, test_set)
client.save_evaluation_scenario_run(results)
