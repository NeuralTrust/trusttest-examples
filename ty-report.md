error[unresolved-import]: Module `trusttest.llm_clients` has no member `HTTPClient`
  --> examples/02_targets/http_llm_client.py:8:35
   |
 6 | from dotenv import load_dotenv
 7 |
 8 | from trusttest.llm_clients import HTTPClient, RetryConfig
   |                                   ^^^^^^^^^^
 9 |
10 | load_dotenv()
   |
info: rule `unresolved-import` is enabled by default

error[unresolved-import]: Module `trusttest.catalog` has no member `MultiTurnManipulationScenario`
 --> examples/03_security_attacks/multi_turn_manipulation.py:5:31
  |
3 | from dotenv import load_dotenv
4 |
5 | from trusttest.catalog import MultiTurnManipulationScenario
  |                               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
6 | from trusttest.probes import Objective
7 | from trusttest.targets.testing import IcantAssistTarget
  |
info: rule `unresolved-import` is enabled by default

error[unresolved-import]: Module `trusttest.llm_clients` has no member `OpenAiClient`
  --> examples/07_evaluators/llm_as_judge.py:12:35
   |
10 |     CorrectnessEvaluator,
11 | )
12 | from trusttest.llm_clients import OpenAiClient
   |                                   ^^^^^^^^^^^^
13 | from trusttest.probes.dataset import DatasetProbe
14 | from trusttest.targets.testing import DummyTarget
   |
info: rule `unresolved-import` is enabled by default

error[unresolved-import]: Module `trusttest.catalog` has no member `CrescendoAttackScenario`
 --> examples/08_scenarios/crescendomation.py:5:31
  |
3 | from dotenv import load_dotenv
4 |
5 | from trusttest.catalog import CrescendoAttackScenario
  |                               ^^^^^^^^^^^^^^^^^^^^^^^
6 | from trusttest.probes import Objective
7 | from trusttest.targets.http import HttpTarget, PayloadConfig
  |
info: rule `unresolved-import` is enabled by default

error[unresolved-import]: Cannot resolve imported module `trusttest.probes.off_topic.disallowed_content`
  --> examples/08_scenarios/disallowed_content_probe.py:10:6
   |
 8 | from trusttest.evaluator_suite import EvaluatorSuite
 9 | from trusttest.evaluators import TrueFalseEvaluator
10 | from trusttest.probes.off_topic.disallowed_content import DisallowedContentDatasetProbe
   |      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
11 | from trusttest.targets.http import HttpTarget, PayloadConfig
   |
info: Searched in the following paths during module resolution:
info:   1. /Users/marti.jorda/Projects/trusttest-examples (first-party code)
info:   2. vendored://stdlib (stdlib typeshed stubs vendored by ty)
info:   3. /Users/marti.jorda/Projects/trusttest-examples/.venv/lib/python3.12/site-packages (site-packages)
info: make sure your Python environment is properly configured: https://docs.astral.sh/ty/modules/#python-environment
info: rule `unresolved-import` is enabled by default

error[unresolved-import]: Cannot resolve imported module `trusttest.probes.off_topic.disallowed_uses`
  --> examples/08_scenarios/disallowed_uses_probe.py:10:6
   |
 8 | from trusttest.evaluator_suite import EvaluatorSuite
 9 | from trusttest.evaluators import TrueFalseEvaluator
10 | from trusttest.probes.off_topic.disallowed_uses import DisallowedUsesDatasetProbe
   |      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
11 | from trusttest.targets.http import HttpTarget, PayloadConfig
   |
info: Searched in the following paths during module resolution:
info:   1. /Users/marti.jorda/Projects/trusttest-examples (first-party code)
info:   2. vendored://stdlib (stdlib typeshed stubs vendored by ty)
info:   3. /Users/marti.jorda/Projects/trusttest-examples/.venv/lib/python3.12/site-packages (site-packages)
info: make sure your Python environment is properly configured: https://docs.astral.sh/ty/modules/#python-environment
info: rule `unresolved-import` is enabled by default

error[unresolved-import]: Module `trusttest.catalog` has no member `EchoChamberAttackScenario`
  --> examples/08_scenarios/echo_chamber_probe.py:8:31
   |
 7 | import trusttest
 8 | from trusttest.catalog import EchoChamberAttackScenario
   |                               ^^^^^^^^^^^^^^^^^^^^^^^^^
 9 | from trusttest.probes import SteeringObjective
10 | from trusttest.targets.http import HttpTarget, PayloadConfig
   |
info: rule `unresolved-import` is enabled by default

error[unresolved-import]: Cannot resolve imported module `trusttest.probes.off_topic.public_figures`
  --> examples/08_scenarios/public_figures_probes.py:10:6
   |
 8 | from trusttest.evaluator_suite import EvaluatorSuite
 9 | from trusttest.evaluators import TrueFalseEvaluator
10 | from trusttest.probes.off_topic.public_figures import PublicFiguresDatasetProbe
   |      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
11 | from trusttest.targets.http import HttpTarget, PayloadConfig
   |
info: Searched in the following paths during module resolution:
info:   1. /Users/marti.jorda/Projects/trusttest-examples (first-party code)
info:   2. vendored://stdlib (stdlib typeshed stubs vendored by ty)
info:   3. /Users/marti.jorda/Projects/trusttest-examples/.venv/lib/python3.12/site-packages (site-packages)
info: make sure your Python environment is properly configured: https://docs.astral.sh/ty/modules/#python-environment
info: rule `unresolved-import` is enabled by default

error[unresolved-import]: Module `trusttest.catalog` has no member `DatasetScenario`
 --> examples/08_scenarios/qa_scenario.py:5:31
  |
3 | from dotenv import load_dotenv
4 |
5 | from trusttest.catalog import DatasetScenario
  |                               ^^^^^^^^^^^^^^^
6 | from trusttest.dataset_builder import DatasetItem, SinglePromptDatasetBuilder
7 | from trusttest.evaluation_contexts import ExpectedResponseContext
  |
info: rule `unresolved-import` is enabled by default

error[unresolved-import]: Module `trusttest.catalog` has no member `RagFunctionalScenario`
 --> examples/10_configuration/custom_llm_parameters.py:6:31
  |
5 | import trusttest
6 | from trusttest.catalog import RagFunctionalScenario
  |                               ^^^^^^^^^^^^^^^^^^^^^
7 | from trusttest.config import Config, EmbeddingsConfig, LLMConfig
8 | from trusttest.evaluators import CorrectnessEvaluator
  |
info: rule `unresolved-import` is enabled by default

error[unresolved-import]: Module `trusttest.catalog` has no member `RagFunctionalScenario`
  --> examples/11_automatic_generation/automatic_test_generation_azure.py:8:31
   |
 6 | from dotenv import load_dotenv
 7 |
 8 | from trusttest.catalog import RagFunctionalScenario
   |                               ^^^^^^^^^^^^^^^^^^^^^
 9 | from trusttest.knowledge_base.azure_search import AzureKnowledgeBase
10 | from trusttest.targets.testing import DummyTarget
   |
info: rule `unresolved-import` is enabled by default

error[unresolved-import]: Module `trusttest.catalog` has no member `RagFunctionalScenario`
 --> examples/11_automatic_generation/automatic_test_generation_basic.py:5:31
  |
3 | from dotenv import load_dotenv
4 |
5 | from trusttest.catalog import RagFunctionalScenario
  |                               ^^^^^^^^^^^^^^^^^^^^^
6 | from trusttest.evaluation_scenarios.base import ProgressInfo
7 | from trusttest.evaluators import CorrectnessEvaluator
  |
info: rule `unresolved-import` is enabled by default

error[unresolved-import]: Module `trusttest.catalog` has no member `RagFunctionalScenario`
 --> examples/11_automatic_generation/automatic_test_generation_neo4j.py:7:31
  |
5 | from dotenv import load_dotenv
6 |
7 | from trusttest.catalog import RagFunctionalScenario
  |                               ^^^^^^^^^^^^^^^^^^^^^
8 | from trusttest.knowledge_base.neo4j import Neo4jKnowledgeBase
9 | from trusttest.targets.testing import DummyTarget
  |
info: rule `unresolved-import` is enabled by default

error[unresolved-import]: Cannot resolve imported module `trusttest.catalog.rag`
 --> examples/11_automatic_generation/automatic_test_generation_postgres.py:7:6
  |
5 | from dotenv import load_dotenv
6 |
7 | from trusttest.catalog.rag import BenignQuestion, RagFunctionalScenario
  |      ^^^^^^^^^^^^^^^^^^^^^
8 | from trusttest.knowledge_base.pgvector import PgVectorKnowledgeBase
9 | from trusttest.targets.testing import DummyTarget
  |
info: Searched in the following paths during module resolution:
info:   1. /Users/marti.jorda/Projects/trusttest-examples (first-party code)
info:   2. vendored://stdlib (stdlib typeshed stubs vendored by ty)
info:   3. /Users/marti.jorda/Projects/trusttest-examples/.venv/lib/python3.12/site-packages (site-packages)
info: make sure your Python environment is properly configured: https://docs.astral.sh/ty/modules/#python-environment
info: rule `unresolved-import` is enabled by default

error[unresolved-import]: Module `trusttest.catalog` has no member `RagPoisoningScenario`
  --> examples/11_automatic_generation/automatic_test_generation_upstash.py:8:31
   |
 7 | import trusttest
 8 | from trusttest.catalog import RagPoisoningScenario
   |                               ^^^^^^^^^^^^^^^^^^^^
 9 | from trusttest.config import Config
10 | from trusttest.knowledge_base.upstash import UpstashKnowledgeBase
   |
info: rule `unresolved-import` is enabled by default

Found 15 diagnostics
