import asyncio
import json
import os
import traceback
import uuid
from datetime import datetime
from pathlib import Path

import httpx
from tqdm import tqdm

REQUEST_TIMEOUT: httpx.Timeout = httpx.Timeout(120.0, connect=30.0)


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def _iter_scenario_dirs(source_dir: Path) -> list[Path]:
    return sorted([path for path in source_dir.iterdir() if path.is_dir()])


def _latest_executions_per_test_case(test_cases: list[dict]) -> list[dict]:
    latest_by_test_case_id: dict[str, dict] = {}
    for test_case in test_cases:
        test_case_id = test_case["test_case_id"]
        execution_date = test_case.get("execution_date", "")
        current = latest_by_test_case_id.get(test_case_id)
        if current is None or execution_date > current.get("execution_date", ""):
            latest_by_test_case_id[test_case_id] = test_case
    return list(latest_by_test_case_id.values())


async def _upload_scenario(
    client: httpx.AsyncClient,
    dest_target_token: str,
    scenario_dir: Path,
    base_url: str,
    target_id: str,
    tests_only: bool,
    semaphore: asyncio.Semaphore,
) -> str | None:
    scenario_id = scenario_dir.name
    target_base = f"{base_url}/v1/evaluation/targets/{target_id}"
    async with semaphore:
        try:
            scenario_path = scenario_dir / "evaluation_scenario.json"
            test_set_path = scenario_dir / "test_set.json"
            eval_run_path = scenario_dir / "evaluation_run.json"

            if not scenario_path.exists():
                raise FileNotFoundError(str(scenario_path))
            if not test_set_path.exists():
                raise FileNotFoundError(str(test_set_path))
            if not tests_only and not eval_run_path.exists():
                raise FileNotFoundError(str(eval_run_path))

            new_scenario = _load_json(scenario_path)
            new_scenario["id"] = str(uuid.uuid4())

            response = await client.post(
                f"{target_base}/scenarios",
                headers={"token": dest_target_token},
                json=new_scenario,
            )
            response.raise_for_status()

            scenario_base = f"{target_base}/scenarios/{new_scenario['id']}"
            test_set = _load_json(test_set_path)
            test_set["id"] = str(uuid.uuid4())
            old_to_new_test_case_ids: dict[str, str] = {}
            for test_case in test_set.get("test_cases", []):
                old_id = test_case["id"]
                new_id = str(uuid.uuid4())
                old_to_new_test_case_ids[old_id] = new_id
                test_case["id"] = new_id
                interactions = test_case.get("interactions", [])
                if interactions and "context" in interactions[0]:
                    test_case["context_keys"] = list(interactions[0]["context"].keys())
                else:
                    test_case["context_keys"] = []
                test_case.pop("last_run", None)
                current_time = datetime.now().isoformat()
                test_case["created_at"] = current_time
                test_case["updated_at"] = current_time

            response = await client.post(
                f"{scenario_base}/test-set",
                headers={"token": dest_target_token},
                json=test_set,
            )
            response.raise_for_status()

            if tests_only:
                return None

            eval_run = _load_json(eval_run_path)
            eval_run["id"] = str(uuid.uuid4())
            for field in ("scenario_id", "page", "limit", "total"):
                eval_run.pop(field, None)
            eval_run["test_cases"] = _latest_executions_per_test_case(
                eval_run.get("test_cases", [])
            )
            for test_case in eval_run["test_cases"]:
                old_test_case_id = test_case["test_case_id"]
                new_test_case_id = old_to_new_test_case_ids[old_test_case_id]
                test_case.pop("id", None)
                test_case["test_case_id"] = new_test_case_id
                test_case["execution_date"] = datetime.now().isoformat()

            response = await client.post(
                f"{scenario_base}/runs",
                headers={"token": dest_target_token},
                json=eval_run,
            )
            response.raise_for_status()
            return None
        except Exception as exc:
            traceback.print_exc()
            tqdm.write(f"Error uploading scenario {scenario_id}: {str(exc)}")
            return scenario_id


async def _upload_tests_async(
    dest_target_token: str,
    scenario_dirs: list[Path],
    base_url: str,
    target_id: str,
    tests_only: bool,
    max_concurrent_requests: int,
    progress_prefix: str = "",
) -> list[str]:
    semaphore = asyncio.Semaphore(max_concurrent_requests)
    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
        tasks = [
            asyncio.create_task(
                _upload_scenario(
                    client=client,
                    dest_target_token=dest_target_token,
                    scenario_dir=scenario_dir,
                    base_url=base_url,
                    target_id=target_id,
                    tests_only=tests_only,
                    semaphore=semaphore,
                )
            )
            for scenario_dir in scenario_dirs
        ]
        error_scenarios: list[str] = []
        for task in tqdm(
            asyncio.as_completed(tasks),
            total=len(tasks),
            desc=f"{progress_prefix}Uploading scenarios",
            unit="scenario",
        ):
            failed_scenario = await task
            if failed_scenario:
                error_scenarios.append(failed_scenario)
        return error_scenarios


def upload_tests(
    dest_target_token: str,
    source_dir: Path,
    target_id: str | None = None,
    base_url: str = "https://control.neuraltrust.ai",
    tests_only: bool = False,
    max_concurrent_requests: int = 4,
    progress_prefix: str = "",
) -> list[str]:
    """Upload evaluation scenarios and related data from local files."""
    base_url = base_url.rstrip("/")
    source_dir = Path(source_dir)
    resolved_target_id = target_id or os.getenv("NEURALTRUST_TARGET_ID")
    if not resolved_target_id:
        raise ValueError(
            "target_id is required when using the control plane API "
            "(or set NEURALTRUST_TARGET_ID)"
        )
    if max_concurrent_requests < 1:
        raise ValueError("max_concurrent_requests must be >= 1")

    scenario_dirs = _iter_scenario_dirs(source_dir)
    return asyncio.run(
        _upload_tests_async(
            dest_target_token=dest_target_token,
            scenario_dirs=scenario_dirs,
            base_url=base_url,
            target_id=resolved_target_id,
            tests_only=tests_only,
            max_concurrent_requests=max_concurrent_requests,
            progress_prefix=progress_prefix,
        )
    )


if __name__ == "__main__":
    dest_target_token = ""
    target_id = "01660e60-7b4a-445e-a310-3ca599c31283"
    source_dir = Path("tests/cbc0437b-319a-464e-8e78-e5e70706e8f0")
    error_scenarios = upload_tests(
        dest_target_token, source_dir, target_id=target_id, tests_only=False
    )
    print(error_scenarios)
