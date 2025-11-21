"""Baseline test for data leakage using multiple sensitive data leak probes with French translation."""

import os

from dotenv import load_dotenv

import trusttest
from trusttest.evaluation_scenarios import EvaluationScenario
from trusttest.evaluator_suite import EvaluatorSuite
from trusttest.evaluators import TrueFalseEvaluator
from trusttest.probes.sensitive_data_leak import (
    DirectQueryForSensitiveDataDatasetProbe,
    ContextualLeakageRequestDatasetProbe,
    MetadataQueryDatasetProbe,
    ObfuscatedDataRequestDatasetProbe,
    MisleadingContextRequestDatasetProbe,
    ListOfAgentAvailableToolsDatasetProbe,
    ListOfParametersOfAgentToolsDatasetProbe,
    ReasoningDetailsOfAiAgentsDatasetProbe,
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
    (DirectQueryForSensitiveDataDatasetProbe, "Direct Query for Sensitive Data"),
    (ContextualLeakageRequestDatasetProbe, "Contextual Leakage Request"),
    (MetadataQueryDatasetProbe, "Metadata Query"),
    (ObfuscatedDataRequestDatasetProbe, "Obfuscated Data Request"),
    (MisleadingContextRequestDatasetProbe, "Misleading Context Request"),
    (ListOfAgentAvailableToolsDatasetProbe, "List of Agent Available Tools"),
    (ListOfParametersOfAgentToolsDatasetProbe, "List of Parameters of Agent Tools"),
    (ReasoningDetailsOfAiAgentsDatasetProbe, "Reasoning Details of AI Agents"),
]

for ProbeClass, category_name in probes:
    probe = ProbeClass(target=target, translate_into_language="French")
    print(f"Testing {category_name}")
    scenario = EvaluationScenario(
        name=f"Data Leak: {category_name}",
        description=f"Test scenario for data leak {category_name}",
        evaluator_suite=EvaluatorSuite(
            evaluators=[TrueFalseEvaluator()],
            criteria="any_fail",
        ),
        category="data-leakage",
        type="data-exfiltration",
    )

    test_set = probe.get_test_set()
    results = scenario.evaluate(test_set)
    results.display_summary()

    client.save_evaluation_scenario(scenario)
    client.save_evaluation_scenario_test_set(scenario.id, test_set)
    client.save_evaluation_scenario_run(results)
