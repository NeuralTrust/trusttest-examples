import asyncio
import json
import os
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from tqdm import tqdm

import trusttest
from trusttest.evaluation_scenarios import EvaluationScenario
from trusttest.evaluator_suite import EvaluatorSuite
from trusttest.evaluators import TrueFalseEvaluator
from trusttest.language_detection.types import LanguageType
from trusttest.probes import Objective
from trusttest.probes.base import TestSet
from trusttest.probes.prompt_injections import (
    AllowedAndDisallowedQuestionsProbe,
    AntiGPTProbe,
    ContextHijackingProbe,
    DANJailbreakProbe,
    EncodedPayloadProbe,
    EncodingAndCapitalizationProbe,
    InstructionalInversionProbe,
    JsonInjectionProbe,
    MultiLanguageAttacksProbe,
    MultimodalInjectionProbe,
    ObfuscationAndTokenSmugglingProbe,
    PayloadSplittingProbe,
    RolePlayingExploitsProbe,
    SymbolicEncodingProbe,
    SynonymsProbe,
    SystemOverrideProbe,
    TypoTricksProbe,
)
from trusttest.targets.http import HttpTarget, PayloadConfig

load_dotenv(override=True)

client = trusttest.client(type="neuraltrust", token=os.getenv("CLIENT_TOKEN"))

target = HttpTarget(
    url="https://api.example.com/chat/banking_french",
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


languages: List[LanguageType] = ["English"]

objectives_data = json.load(open(Path(".") / "default-malicious-objectives.json"))
objectives: List[Objective] = [
    Objective(
        question=objective["objective"],
        true_description=objective["true_description"],
        false_description=objective["false_description"],
    )
    for objective in objectives_data
]

probes = [
    ("allowed_and_disallowed_questions", AllowedAndDisallowedQuestionsProbe),
    ("antigpt", AntiGPTProbe),
    ("context_hijacking", ContextHijackingProbe),
    ("dan_jailbreak", DANJailbreakProbe),
    ("encoded_payload", EncodedPayloadProbe),
    ("encoding_and_capitalization", EncodingAndCapitalizationProbe),
    ("instructional_inversion", InstructionalInversionProbe),
    ("json_injection", JsonInjectionProbe),
    ("multi_language_attacks", MultiLanguageAttacksProbe),
    ("multimodal_injection", MultimodalInjectionProbe),
    ("obfuscation_and_token_smuggling", ObfuscationAndTokenSmugglingProbe),
    ("payload_splitting", PayloadSplittingProbe),
    ("role_playing_exploits", RolePlayingExploitsProbe),
    ("symbolic_encoding", SymbolicEncodingProbe),
    ("synonyms", SynonymsProbe),
    ("system_override", SystemOverrideProbe),
    ("typo_tricks", TypoTricksProbe),
]


async def process_probe(
    probe_name: str, probe_class: type, language: LanguageType
) -> None:
    """Process a single probe by generating test sets for all objectives in parallel."""
    print(f"Generating dataset for {probe_name}...")
    probes = [
        probe_class(
            target=target, objectives=[objective], language=language, num_items=1
        )
        for objective in objectives
    ]

    tasks = [probe.async_get_test_set() for probe in probes]
    test_sets = []
    with tqdm(total=len(tasks), desc=f"  {probe_name} objectives", leave=False) as pbar:
        for coro in asyncio.as_completed(tasks):
            test_set = await coro
            test_sets.append(test_set)
            pbar.update(1)

    test_set = TestSet.union(test_sets)

    output_dir = f"datasets/{language}/prompt_injections/{probe_name}"
    os.makedirs(output_dir, exist_ok=True)

    output_file = f"{output_dir}/test_set.json"
    with open(output_file, "w") as f:
        json.dump(test_set.to_dict(), f, indent=2)

    scenario = EvaluationScenario(
        name=f"{probe_name} Attack",
        description=f"Test scenario for {probe_name} attack",
        evaluator_suite=EvaluatorSuite(
            evaluators=[TrueFalseEvaluator()],
            criteria="any_fail",
        ),
        category="prompt-injections",
    )

    results = scenario.evaluate(test_set)
    results.display_summary()

    client.save_evaluation_scenario(scenario)
    client.save_evaluation_scenario_test_set(scenario.id, test_set)
    client.save_evaluation_scenario_run(results)


async def main() -> None:
    """Main async function to process all probes."""
    for language in languages:
        for probe_name, probe_class in tqdm(probes, desc="Processing probes"):
            await process_probe(probe_name, probe_class, language)

        print(f"\nDone generating all datasets for {language}!")


if __name__ == "__main__":
    asyncio.run(main())
