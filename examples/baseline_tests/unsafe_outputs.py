"""Baseline test for unsafe outputs using multiple toxicity probes (hate, crimes, defamation, etc.) with French translation."""

import os

from dotenv import load_dotenv

import trusttest
from trusttest.evaluation_scenarios import EvaluationScenario
from trusttest.evaluator_suite import EvaluatorSuite
from trusttest.evaluators import TrueFalseEvaluator
from trusttest.probes import (
    ChildSexualExploitationDatasetProbe,
    DefamationDatasetProbe,
    HateDatasetProbe,
    IndiscriminateWeaponsDatasetProbe,
    IntellectualPropertyDatasetProbe,
    NonViolentCrimesDatasetProbe,
    SexRelatedCrimesDatasetProbe,
    SuicideAndSelfHarmDatasetProbe,
    ViolentCrimesDatasetProbe,
)
from trusttest.targets.http import HttpTarget, PayloadConfig

load_dotenv(override=True)


client = trusttest.client(type="neuraltrust", token=os.getenv("NEURALTURST_TOKEN"))


target = HttpTarget(
    url="https://my-llm/chat_french",
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

probes = [
    (HateDatasetProbe, "Hate"),
    (NonViolentCrimesDatasetProbe, "Non Violent Crimes"),
    (DefamationDatasetProbe, "Defamation"),
    (IntellectualPropertyDatasetProbe, "Intellectual Property"),
    (IndiscriminateWeaponsDatasetProbe, "Indiscriminate Weapons"),
    (SuicideAndSelfHarmDatasetProbe, "Suicide And Self Harm"),
    (ChildSexualExploitationDatasetProbe, "Child Sexual Exploitation"),
    (SexRelatedCrimesDatasetProbe, "Sex Related Crimes"),
    (ViolentCrimesDatasetProbe, "Violent Crimes"),
]

for probe_class, category_name in probes:
    probe = probe_class(target=target, translate_into_language="French")
    print(f"Testing {category_name}")
    scenario = EvaluationScenario(
        name=f"Responsibility: {category_name}",
        description=f"Test scenario for unsafe output {category_name}",
        evaluator_suite=EvaluatorSuite(
            evaluators=[TrueFalseEvaluator()],
            criteria="any_fail",
        ),
        category="responsibility",
        type="toxicity",
    )

    test_set = probe.get_test_set()
    results = scenario.evaluate(test_set)
    results.display_summary()

    client.save_evaluation_scenario(scenario)
    client.save_evaluation_scenario_test_set(scenario.id, test_set)
    client.save_evaluation_scenario_run(results)
