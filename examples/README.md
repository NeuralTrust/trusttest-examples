# Examples Directory Structure

This directory contains organized examples demonstrating various features and use cases of TrustTest.

## Folder Organization

### 01_getting_started/
Basic examples for getting started with TrustTest:
- `quickstart.py` - Quickstart guide with basic evaluation scenario
- `basic_run.py` - Basic evaluation run example
- `basic_run_2.py` - Alternative basic run example
- `basic_scenario.py` - Basic scenario setup example

### 02_targets/
Examples demonstrating different target/client configurations:
- `http_llm_client.py` - HTTP LLM client configuration
- `http_endpoint.py` - HTTP endpoint target example
- `http_stream.py` - HTTP streaming example
- `local_llm.py` - Local LLM target configuration
- `ollama_model.py` - Ollama model integration
- `groq_api.py` - Groq API integration
- `deepseek.py` - DeepSeek API integration
- `default_client.py` - Default client configuration

### 03_evaluators/
Custom evaluator examples:
- `custom_evaluator_expected_response.py` - Custom evaluator with expected responses
- `llm_as_judge.py` - Using LLM as a judge/evaluator

### 04_probes/
Probe examples for security testing, bias detection, and evaluation scenarios:

**Security attack probes:**
- `xss_attack_vector.py` - XSS attack detection
- `json_injection.py` - JSON injection attacks
- `context_hijacking.py` - Context hijacking attacks
- `system_override.py` - System prompt override attempts
- `system_prompt_disclosure.py` - System prompt disclosure tests
- `system_prompt_disclosure_prompt.py` - Prompt-based disclosure tests
- `dan_jailbreak.py` - DAN jailbreak attempts
- `antigpt.py` - Anti-GPT attack examples
- `role_playing_exploits.py` - Role-playing exploit attempts
- `encoded_payload.py` - Encoded payload attacks
- `encoding_and_capitalization.py` - Encoding/capitalization obfuscation
- `obfuscation_and_token_smuggling.py` - Token smuggling techniques
- `payload_splitting.py` - Payload splitting attacks
- `symbolic_encoding.py` - Symbolic encoding attacks
- `multimodal_injection.py` - Multimodal injection attacks
- `input_leak.py` - Input leakage detection
- `sensitive_data_leak.py` - Sensitive data leak detection
- `sensitive_data_leak_prompt.py` - Prompt-based data leak tests
- `virus_output.py` - Virus/malware output detection
- `multi_turn_manipulation.py` - Multi-turn conversation manipulation
- `typo_tricks.py` - Typo-based attack techniques
- `crescendomation.py` - Crescendo attack scenario

**Bias probes:**
- `framing_bias.py` - Framing bias detection
- `positional_bias.py` - Positional bias testing
- `anchoring_bias.py` - Anchoring bias examples
- `status_quo_bias.py` - Status quo bias detection
- `temporal_bias.py` - Temporal bias testing
- `stereotypical_bias.py` - Stereotypical bias detection
- `bias_prompt.py` - Prompt-based bias testing

**Evaluation scenario probes:**
- `qa_scenario.py` - Q&A scenario example
- `competitor_check.py` - Competitor mention detection scenario
- `competitor_check_prompt.py` - Prompt-based competitor check
- `correct_url.py` - URL correctness evaluation
- `test_url_correct.py` - URL correctness test suite
- `echo_chamber_probe.py` - Echo chamber attack probe
- `disallowed_content_probe.py` - Disallowed content detection
- `disallowed_uses_probe.py` - Disallowed uses detection
- `unsafe_outputs_probe.py` - Unsafe outputs detection
- `unsafe_outputs_prompt.py` - Prompt-based unsafe outputs test
- `public_figures_probes.py` - Public figures information disclosure
- `dataset_probe.py` - Dataset-based probing
- `prompt_dataset_probe.py` - Prompt-based dataset probing
- `allowed_and_disallowed_questions.py` - Allowed/disallowed question filtering
- `agentic_behavior_limits.py` - Agentic behavior limit testing
- `synonyms.py` - Synonym-based testing

### 05_rag_poisoning/
RAG (Retrieval-Augmented Generation) poisoning examples:
- `rag_poisoning.py` - RAG poisoning attack examples
- `test_rag_poisoning.py` - RAG poisoning test suite
- `automatic_test_generation_basic.py` - Automatic RAG test generation with in-memory knowledge base

### 06_functional_tests/
Automatic functional test generation examples with various backends:
- `automatic_test_generation_basic.py` - Basic automatic test generation
- `automatic_test_generation_azure.py` - Azure-based test generation
- `automatic_test_generation_neo4j.py` - Neo4j-based test generation
- `automatic_test_generation_postgres.py` - PostgreSQL-based test generation
- `automatic_test_generation_upstash.py` - Upstash-based test generation

### 07_dataset_building/
Dataset building and construction examples:
- `dataset_builder_conversation.py` - Conversation dataset builder
- `dataset_builder_conversation_2.py` - Alternative conversation builder
- `dataset_builder_conversation_3.py` - Another conversation builder variant
- `dataset_builder_expected_response.py` - Expected response dataset builder
- `dataset_builder_objective.py` - Objective-based dataset builder
- `dataset_builder_objective_2.py` - Alternative objective builder
- `static_dataset.py` - Static dataset examples

### 09_red_team/
Red teaming examples using the TrustTest red-team catalog (HTTP targets, scenarios, and helpers):
- `basic_red_teaming.py` - Minimal red-team run
- `agentic_behavior/run_scenarios.py` - Agentic behavior scenarios
- `bias/run_dataset_scenarios.py`, `bias/run_objective_scenarios.py` - Bias scenarios (dataset and objective flows)
- `functional/run_scenario.py`, `functional/pdf_to_chunks.py` - Functional / RAG-style scenarios and PDF chunking helper
- `input_leakage/run_scenarios.py` - Input leakage scenarios
- `off_topic/run_scenarios.py` - Off-topic scenarios
- `prompt_injections/single_turn.py`, `prompt_injections/multi_turn.py` - Prompt injection scenarios
- `rag_poisonig/run_scenario.py`, `rag_poisonig/pdf_to_chunks.py` - RAG poisoning scenarios and PDF helper
- `sensitive_data_leak/run_scenarios.py` - Sensitive data leak scenarios
- `system_prompt_disclosure/run_scenarios.py` - System prompt disclosure scenarios
- `unsafe_outputs/run_scenarios.py` - Unsafe outputs scenarios

### 10_platform_api/
Platform API utilities for syncing and running tests with the NeuralTrust control plane:
- `clone_team.py` - Clone evaluation scenarios and related data between targets
- `download_tests.py` - Download test cases and evaluation results from the platform
- `upload_tests.py` - Upload test cases and scenarios to the platform
- `evaluate_local.py` - Run evaluations locally against downloaded scenario/test-set files
- `run_all_scenarios.py` - Execute all scenarios for a target via the platform API

### data/
Dataset files used by examples:
- `qa_dataset.json` - Q&A dataset in JSON format
- `qa_dataset.parquet` - Q&A dataset in Parquet format

## Usage

Most examples can be run directly from the project root:

```bash
python examples/01_getting_started/quickstart.py
```

Note: Some examples require environment variables to be set (API keys, `NEURALTRUST_TOKEN`, `NEURALTRUST_TARGET_ID`, etc.). Check individual files for specific requirements.
