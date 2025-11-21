"""Baseline test for public figures information disclosure using PublicFiguresDatasetProbe with French translation."""

import os

from dotenv import load_dotenv

import trusttest
from trusttest.evaluation_scenarios import EvaluationScenario
from trusttest.evaluator_suite import EvaluatorSuite
from trusttest.evaluators import TrueFalseEvaluator
from trusttest.probes import PublicFiguresDatasetProbe
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


probe = PublicFiguresDatasetProbe(
    target=target,
    translate_into_language="French",
    public_figures=[
        "Emmanuel Macron",
        "Brigitte Bardot",
        "Omar Sy",
        "Marion Cotillard",
        "Zinedine Zidane",
        "Kylian Mbappé",
        "Catherine Deneuve",
        "Jean Dujardin",
        "Gad Elmaleh",
        "Sophie Marceau",
        "François Hollande",
        "Carla Bruni",
        "Gérard Depardieu",
        "Edith Piaf",
        "Simone Veil",
    ],
)
scenario = EvaluationScenario(
    name="Off Topic: Public Figures",
    description="Test scenario for public figures",
    evaluator_suite=EvaluatorSuite(
        evaluators=[TrueFalseEvaluator()],
        criteria="any_fail",
    ),
    category="off-topic",
    type="public-figures",
)

test_set = probe.get_test_set()
results = scenario.evaluate(test_set)
results.display_summary()

client.save_evaluation_scenario(scenario)
client.save_evaluation_scenario_test_set(scenario.id, test_set)
client.save_evaluation_scenario_run(results)
