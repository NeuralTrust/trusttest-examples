"""Example demonstrating evaluation run execution and metrics retrieval.

This example shows how to:
1. Run evaluation scenarios (all test cases or single test case)
2. Monitor evaluation run status in real-time
3. Get test set status
4. Retrieve scenario metrics with historical data
5. Get aggregated target metrics across all scenarios

Endpoints demonstrated:
- POST /evaluation-scenario/{id}/run
- POST /evaluation-scenario/{id}/test-case/{id}/run
- GET /evaluation-scenario/{id}/evaluation-run/{id}/status
- GET /evaluation-scenario/{id}/test-set/status
- GET /evaluation-scenario/{id}/metrics
- GET /target/total-metrics
"""

import os
from datetime import datetime, timedelta

from dotenv import load_dotenv

import trusttest
from trusttest.clients import (
    EvaluationRunStatus,
    RunResult,
    ScenarioMetrics,
    TargetMetrics,
    TestSetStatus,
)
from trusttest.dataset_builder import Dataset
from trusttest.evaluation_contexts import ExpectedResponseContext
from trusttest.evaluation_scenarios import EvaluationScenario
from trusttest.evaluator_suite import EvaluatorSuite
from trusttest.evaluators import CorrectnessEvaluator
from trusttest.probes import DatasetProbe
from trusttest.targets.http import HttpTarget, PayloadConfig

load_dotenv(override=True)

os.environ["NEURALTRUST_BASE_URL"] = "https://example.com/v1/evaluation"

client = trusttest.client(
    type="neuraltrust",
    token=os.getenv("NEURALTRUST_TOKEN"),
    target_id=os.getenv("NEURALTRUST_TARGET_ID"),
    verify=False,
)

model = HttpTarget(
    url="https://example.com/api/chat",
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
    },
    payload_config=PayloadConfig(
        format={
            "model": "o4-mini-2025-04-16",
            "messages": [
                {
                    "role": "user",
                    "content": "{{ test }}",
                }
            ],
        },
        message_regex="{{ test }}",
        timeout=60,
    ),
    concatenate_field="choices.0.message.content",
)

dataset_path = "examples/data/qa_dataset.json"
dataset: Dataset[ExpectedResponseContext] = Dataset.from_json(path=dataset_path)
probe = DatasetProbe(target=model, dataset=dataset)

scenario = EvaluationScenario(
    description="Demonstration of evaluation runs and metrics endpoints",
    name="Evaluation Runs & Metrics Example",
    evaluator_suite=EvaluatorSuite(
        evaluators=[CorrectnessEvaluator()],
        criteria="any_fail",
    ),
)

test_set = probe.get_test_set()
results = scenario.evaluate(test_set)
results.display_summary()

client.save_evaluation_scenario(scenario)
client.save_evaluation_scenario_test_set(scenario.id, test_set)
client.save_evaluation_scenario_run(results)

print("\n1. Run evaluation scenario")
run_result: RunResult | None = None
try:
    run_result = client.run_evaluation_scenario(
        scenario_id=scenario.id,
        refresh_responses=True,
        notify=False,
    )
    print(f"   ✓ Run ID: {run_result.id}")
except Exception as e:
    print(f"   ✗ Error: {e}")

if test_set.test_cases:
    print("\n2. Run single test case")
    try:
        test_case_id = test_set.test_cases[0].id
        test_case_result: RunResult = client.run_evaluation_scenario_test_case(
            scenario_id=scenario.id,
            test_case_id=test_case_id,
            refresh_responses=True,
            notify=False,
        )
        print(f"   ✓ Run ID: {test_case_result.id}")
    except Exception as e:
        print(f"   ✗ Error: {e}")

if run_result:
    print("\n3. Get evaluation run status")
    try:
        run_status: EvaluationRunStatus = client.get_evaluation_run_status(
            scenario_id=scenario.id,
            evaluation_run_id=run_result.id,
            timeout=5000,
        )
        print(f"   ✓ Status: {run_status.status}")
        print(f"   ✓ Run ID: {run_status.run_id}")
        if run_status.progress:
            prog = run_status.progress
            print(
                f"   ✓ Progress: {prog.get('completed_test_cases', 0)}/{prog.get('total_test_cases', 0)} ({prog.get('completion_percentage', 0):.2f}%)"
            )
    except Exception as e:
        print(f"   ✗ Error: {e}")

print("\n4. Get test set status")
try:
    test_set_status: TestSetStatus = client.get_evaluation_test_set_status(
        scenario_id=scenario.id,
        timeout=5000,
    )
    print(f"   ✓ Status: {test_set_status.status}")
    print(f"   ✓ Scenario ID: {test_set_status.scenario_id}")
    print(f"   ✓ Target ID: {test_set_status.target_id}")
    if test_set_status.progress:
        print(f"   ✓ Progress: {test_set_status.progress}")
except Exception as e:
    print(f"   ✗ Error: {e}")

print("\n5. Get scenario metrics (last 30 days)")
try:
    from_date = datetime.now() - timedelta(days=30)
    to_date = datetime.now()
    metrics: ScenarioMetrics = client.get_evaluation_scenario_run_metrics(
        scenario_id=scenario.id,
        from_date=from_date,
        to_date=to_date,
    )
    print(f"   ✓ Total: {metrics.total_test_cases}")
    print(f"   ✓ Executed: {metrics.total_test_cases_executed}")
    print(f"   ✓ Passed: {metrics.total_passed_test_cases}")
    print(f"   ✓ Failed: {metrics.total_failed_test_cases}")
    print(f"   ✓ Pass rate: {metrics.percentage_passed:.2f}%")
    if metrics.last_run_at:
        print(f"   ✓ Last run: {metrics.last_run_at}")
except Exception as e:
    print(f"   ✗ Error: {e}")

print("\n6. Get target total metrics")
try:
    target_metrics: TargetMetrics = client.get_target_total_metrics(
        to_date=datetime.now()
    )
    print(f"   ✓ Target ID: {target_metrics.target_id}")
    print(f"   ✓ Total: {target_metrics.total_test_cases}")
    print(f"   ✓ Executed: {target_metrics.total_test_cases_executed}")
    print(f"   ✓ Passed: {target_metrics.total_passed_test_cases}")
    print(f"   ✓ Failed: {target_metrics.total_failed_test_cases}")
    print(f"   ✓ Pass rate: {target_metrics.percentage_passed:.2f}%")
    if target_metrics.last_run_at:
        print(f"   ✓ Last run: {target_metrics.last_run_at}")
except Exception as e:
    print(f"   ✗ Error: {e}")

print("\n" + "=" * 80)
print("Example completed!")
print("\nNote: This example uses OpenAI's API via HttpTarget.")
print("Make sure OPENAI_API_KEY is set in your .env file.")
