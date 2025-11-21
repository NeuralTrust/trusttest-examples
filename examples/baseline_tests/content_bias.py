"""Baseline test for content bias using multiple stereotypical bias probes (ethnic, gender, LGBTQ+, religion)."""

import os

from dotenv import load_dotenv

import trusttest
from trusttest.evaluation_scenarios import EvaluationScenario
from trusttest.evaluator_suite import EvaluatorSuite
from trusttest.evaluators import TrueFalseEvaluator
from trusttest.probes import (
    EthnicStereotypicalBiasDatasetProbe,
    GenderStereotypicalBiasDatasetProbe,
    LgtbiqStereotypicalBiasDatasetProbe,
    ReligionStereotypicalBiasDatasetProbe,
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
        rate_limit=1,
        timeout=60,
        format={
            "message": "{{ test }}",
        },
    ),
    concatenate_field="response",
)


probes = [
    (EthnicStereotypicalBiasDatasetProbe, "Ethnic Stereotypical Bias"),
    (GenderStereotypicalBiasDatasetProbe, "Gender Stereotypical Bias"),
    (LgtbiqStereotypicalBiasDatasetProbe, "Lgtbiq Stereotypical Bias"),
    (ReligionStereotypicalBiasDatasetProbe, "Religion Stereotypical Bias"),
]

for ProbeClass, category_name in probes:
    probe = ProbeClass(target=target, translate_into_language="French")
    print(f"Testing {category_name}")
    scenario = EvaluationScenario(
        name=f"Bias: {category_name}",
        description=f"Test scenario for bias {category_name}",
        evaluator_suite=EvaluatorSuite(
            evaluators=[TrueFalseEvaluator()],
            criteria="any_fail",
        ),
        category="content_bias",
        type="content_bias",
    )

    test_set = probe.get_test_set()
    results = scenario.evaluate(test_set)
    results.display_summary()

    client.save_evaluation_scenario(scenario)
    client.save_evaluation_scenario_test_set(scenario.id, test_set)
    client.save_evaluation_scenario_run(results)
