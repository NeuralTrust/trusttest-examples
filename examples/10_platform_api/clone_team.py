import time
import uuid
from datetime import datetime

import httpx
from tqdm import tqdm

REQUEST_TIMEOUT: httpx.Timeout = httpx.Timeout(120.0, connect=30.0)


def clone_tests(
    org_target_token: str,
    dest_target_token: str,
    source_target_id: str,
    dest_target_id: str,
    base_url: str = "https://control.neuraltrust.ai",
    tests_only: bool = False,
) -> list[str]:
    """Clone evaluation scenarios and related data between targets."""
    base_url = base_url.rstrip("/")
    source_base = f"{base_url}/v1/evaluation/targets/{source_target_id}"
    dest_base = f"{base_url}/v1/evaluation/targets/{dest_target_id}"
    url = f"{source_base}/scenarios/view?limit=1000"
    with httpx.Client(timeout=REQUEST_TIMEOUT) as client:
        response = client.get(url, headers={"token": org_target_token})
        response.raise_for_status()
        scenarios_view = response.json()

        scenario_ids = [
            scenario["id"]
            for scenario in scenarios_view.get("evaluation_scenarios", [])
        ]
        error_scenarios: list[str] = []

        for old_scenario_id in tqdm(
            scenario_ids, desc="Cloning scenarios", unit="scenario"
        ):
            try:
                response = client.get(
                    f"{source_base}/scenarios/{old_scenario_id}",
                    headers={"token": org_target_token},
                )
                response.raise_for_status()
                new_scenario = response.json()
                new_scenario["id"] = str(uuid.uuid4())

                response = client.post(
                    f"{dest_base}/scenarios",
                    headers={"token": dest_target_token},
                    json=new_scenario,
                )
                response.raise_for_status()

                test_set_response = client.get(
                    f"{source_base}/scenarios/{old_scenario_id}/test-set?limit=1000",
                    headers={"token": org_target_token},
                )
                test_set_response.raise_for_status()
                test_set = test_set_response.json()
                test_set["id"] = str(uuid.uuid4())
                old_to_new_test_case_ids: dict[str, str] = {}
                for test_case in test_set["test_cases"]:
                    old_id = test_case["id"]
                    new_id = str(uuid.uuid4())
                    old_to_new_test_case_ids[old_id] = new_id
                    test_case["id"] = new_id
                    interactions = test_case.get("interactions", [])
                    if interactions and "context" in interactions[0]:
                        test_case["context_keys"] = list(
                            interactions[0]["context"].keys()
                        )
                    else:
                        test_case["context_keys"] = []
                    test_case.pop("last_run", None)
                    current_time = datetime.now().isoformat()
                    test_case["created_at"] = current_time
                    test_case["updated_at"] = current_time

                time.sleep(1)

                scenario_base = f"{dest_base}/scenarios/{new_scenario['id']}"
                response = client.post(
                    f"{scenario_base}/test-set",
                    headers={"token": dest_target_token},
                    json=test_set,
                )
                response.raise_for_status()

                if not tests_only:
                    eval_run_response = client.get(
                        f"{source_base}/scenarios/{old_scenario_id}/runs?limit=10000",
                        headers={"token": org_target_token},
                    )
                    eval_run_response.raise_for_status()
                    eval_run = eval_run_response.json()
                    eval_run["id"] = str(uuid.uuid4())
                    for field in ("scenario_id", "page", "limit", "total"):
                        eval_run.pop(field, None)
                    for test_case in eval_run.get("test_cases", []):
                        old_test_case_id = test_case["test_case_id"]
                        new_test_case_id = old_to_new_test_case_ids[old_test_case_id]
                        test_case.pop("id", None)
                        test_case["test_case_id"] = new_test_case_id
                        test_case["execution_date"] = datetime.now().isoformat()

                    response = client.post(
                        f"{scenario_base}/runs",
                        headers={"token": dest_target_token},
                        json=eval_run,
                    )
                    response.raise_for_status()

                time.sleep(1)
            except Exception as exc:
                tqdm.write(f"Error cloning scenario {old_scenario_id}: {exc}")
                error_scenarios.append(old_scenario_id)
                time.sleep(2)

        return error_scenarios


if __name__ == "__main__":
    dest_target_token = ""
    org_target_token = ""
    source_target_id = "cbc0437b-319a-464e-8e78-e5e70706e8f0"
    dest_target_id = "eb3e5a10-d6f9-48a6-950d-6492c5dde21e"
    error_scenarios = clone_tests(
        org_target_token,
        dest_target_token,
        source_target_id,
        dest_target_id,
    )
    print(error_scenarios)
