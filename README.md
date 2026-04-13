# TrustTest Examples

This repository contains example code and tutorials demonstrating how to use TrustTest for LLM functional evaluation and red teaming.

For more information about TrustTest, please visit the [TrustTest documentation](https://docs.neuraltrust.ai/trusttest/getting-started/overview).

## Installation

To install TrustTest python package you will need the credentials to access our private Python package repository. **Please contact us to get the credentials.**

```bash
export GOOGLE_APPLICATION_CREDENTIALS=pypi_private.json
export UV_KEYRING_PROVIDER=subprocess
uv tool install keyring --with keyrings.google-artifactregistry-auth

uv sync
# install all optional dependencies
uv sync --all-extras
```

## Examples Directory Structure

The `examples/` directory contains organized examples demonstrating various features and use cases of TrustTest. The examples are organized into the following folders:

- **01_getting_started/** - Basic examples for getting started with TrustTest (quickstart, basic runs, scenarios)
- **02_targets/** - Examples demonstrating different target/client configurations (HTTP, local LLM, Ollama, Groq, DeepSeek, etc.)
- **03_security_attacks/** - Security attack vector examples and probes (XSS, injection attacks, jailbreaks, data leaks, etc.)
- **04_bias/** - Bias testing examples (framing, positional, anchoring, temporal, stereotypical bias)
- **05_rag/** - RAG (Retrieval-Augmented Generation) related examples and poisoning attacks
- **06_dataset_building/** - Dataset building and construction examples
- **07_evaluators/** - Custom evaluator examples and LLM-as-judge patterns
- **08_scenarios/** - Evaluation scenario examples (competitor checks, URL correctness, probes, etc.)
- **09_utilities/** - Utility scripts and helpers (save/load results, rate limiting, multi-language support)
- **10_configuration/** - Configuration examples for custom LLM parameters and HTTP settings
- **11_automatic_generation/** - Automatic test generation examples with various backends (Azure, Neo4j, PostgreSQL, Upstash)
- **12_red_team/** - Red teaming examples using the TrustTest red-team catalog (scenarios, HTTP targets, helpers)

Most examples can be run directly from the project root:

```bash
python examples/01_getting_started/quickstart.py
```

For detailed information about each folder and its contents, see [examples/README.md](examples/README.md).

## Development

We use [pre-commit](https://pre-commit.com/) to run linting and formatting checks. You can get it by using ``brew install pre-commit``. You can then install it in the project with the following command:

```bash
pre-commit install
```

When you make changes to the code, you can run the following command to run the linting and formatting checks:

```bash
ruff check . --fix && ruff format .
mypy .
```
