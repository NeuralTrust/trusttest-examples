# TrustTest Examples

Build confidence in your LLM applications with hands-on TrustTest examples for functional evaluation, red teaming, and safer releases.

Explore ready-to-run workflows, adapt them to your own targets, and learn more in the [TrustTest documentation](https://docs.neuraltrust.ai/trusttest/getting-started/overview).

## Usage

To run a base Red Teaming scenario, you can use the following code:

```python
import os
from typing import List

from dotenv import load_dotenv

import trusttest
from trusttest.catalog.red_team import run_red_teaming
from trusttest.language_detection.types import LanguageType
from trusttest.targets.http import HttpTarget, PayloadConfig

load_dotenv(override=True)


target = HttpTarget(
    url="https://your-api.com/chat",
    headers={"Content-Type": "application/json"},
    payload_config=PayloadConfig(format={"message": "{{ test }}"}),
    concatenate_field="response",
)

client = trusttest.client(type="neuraltrust", token=os.getenv("TARGET_TOKEN"), target_id=os.getenv("NEURALTRUST_TARGET_ID"))

languages: List[LanguageType] = ["English"]
for language in languages:
    run_red_teaming(
        target, language=language, client=client, num_test_cases=50, evaluate=False
    )
```

Or go much deeper and create your own custom scenario:

```python
from trusttest.dataset_builder import Dataset
from trusttest.evaluation_contexts import ExpectedResponseContext
from trusttest.evaluation_scenarios import EvaluationScenario
from trusttest.evaluator_suite import EvaluatorSuite
from trusttest.evaluators import CompletenessEvaluator, CorrectnessEvaluator
from trusttest.probes import DatasetProbe
from trusttest.targets.http import HttpTarget, PayloadConfig

target = HttpTarget(
    url="https://your-api.com/chat",
    headers={"Content-Type": "application/json"},
    payload_config=PayloadConfig(format={"message": "{{ test }}"}),
    concatenate_field="response",
)

dataset: Dataset[ExpectedResponseContext] = Dataset.from_json(path="data/qa_dataset.json")
probe = DatasetProbe(target=target, dataset=dataset)

scenario = EvaluationScenario(
    description="Evaluate model responses",
    name="QA Evaluation",
    evaluator_suite=EvaluatorSuite(
        evaluators=[
            CorrectnessEvaluator(threshold=4),
            CompletenessEvaluator(threshold=4),
        ],
        criteria="any_fail",
    ),
)

test_set = probe.get_test_set()
results = scenario.evaluate(test_set)
results.display_summary()
```

## Installation

To install TrustTest you need credentials for our private Python package repository. **Please contact us to get access.**

For full instructions, see the [How to Install TrustTest](https://docs.neuraltrust.ai/trusttest/getting-started/installation).

If your GCP account have direct access to Neuraltrust Artifact Registry:

```bash
gcloud auth login
make install
```

`make install` configures Artifact Registry auth (keyring), creates the virtual environment (`uv sync --all-extras`), and installs pre-commit hooks.

## Examples Directory Structure

The `examples/` directory contains organized examples demonstrating various features and use cases of TrustTest. The examples are organized into the following folders:

- **01_getting_started/** - Basic examples for getting started with TrustTest (quickstart, basic runs, scenarios)
- **02_targets/** - Examples demonstrating different target/client configurations (HTTP, local LLM, Ollama, Groq, DeepSeek, etc.)
- **03_evaluators/** - Custom evaluator examples and LLM-as-judge patterns
- **04_probes/** - Probe examples for security testing, bias detection, and evaluation scenarios (XSS, injection attacks, jailbreaks, competitor checks, URL correctness, etc.)
- **05_rag_poisoning/** - RAG poisoning attack examples and automatic RAG test generation
- **06_functional_tests/** - Automatic functional test generation with various backends (Azure, Neo4j, PostgreSQL, Upstash)
- **07_dataset_building/** - Dataset building and construction examples
- **09_red_team/** - Red teaming examples using the TrustTest red-team catalog (scenarios, HTTP targets, helpers)
- **10_platform_api/** - Platform API utilities for syncing and running tests with the NeuralTrust control plane (clone, upload, download, local evaluation)

Most examples can be run directly from the project root:

```bash
python examples/01_getting_started/quickstart.py
```

For detailed information about each folder and its contents, see [examples/README.md](examples/README.md).

## Development

Install the virtual environment and pre-commit hooks:

```bash
make install
```

Run linting, formatting, and type checks:

```bash
make lint
```

This runs [Ruff](https://docs.astral.sh/ruff/) (lint + format) and [ty](https://docs.astral.sh/ty/) type checking. [pre-commit](https://pre-commit.com/) hooks are installed by `make install` and run the same checks on commit.
