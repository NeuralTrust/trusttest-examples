import asyncio
import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import httpx
from tqdm import tqdm


def _format_api_date(dt: datetime) -> str:
    dt = dt.astimezone(timezone.utc)
    return dt.isoformat(timespec="milliseconds").replace("+00:00", "Z")


def _date_range() -> tuple[str, str]:
    local_tz = ZoneInfo("Europe/Madrid")
    now_local = datetime.now(local_tz)
    end_local = now_local.replace(hour=23, minute=59, second=59, microsecond=999000)
    start_date = now_local.date() - timedelta(days=30)
    start_local = datetime(
        start_date.year, start_date.month, start_date.day, tzinfo=local_tz
    )
    return (
        _format_api_date(start_local),
        _format_api_date(end_local),
    )


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2, sort_keys=True)
        file.write("\n")


async def _download_scenario(
    client: httpx.AsyncClient,
    org_target_token: str,
    output_dir: Path,
    base_url: str,
    target_id: str,
    scenario_id: str,
    tests_only: bool,
    semaphore: asyncio.Semaphore,
) -> str | None:
    scenario_base = (
        f"{base_url}/v1/evaluation/targets/{target_id}/scenarios/{scenario_id}"
    )
    async with semaphore:
        try:
            response = await client.get(
                scenario_base,
                headers={"token": org_target_token},
            )
            response.raise_for_status()
            evaluation_scenario = response.json()

            scenario_dir = output_dir / target_id / scenario_id
            _write_json(
                scenario_dir / "evaluation_scenario.json",
                evaluation_scenario,
            )

            day_start, day_end = _date_range()
            test_set_response = await client.get(
                f"{scenario_base}/test-set",
                params={"fromDate": day_start, "toDate": day_end},
                headers={"token": org_target_token},
            )
            test_set_response.raise_for_status()
            test_set = test_set_response.json()
            _write_json(scenario_dir / "test_set.json", test_set)

            if tests_only:
                return None

            eval_run_response = await client.get(
                f"{scenario_base}/runs",
                params={
                    "limit": 10000,
                    "runAt": f"between:{day_start},{day_end}",
                },
                headers={"token": org_target_token},
            )
            eval_run_response.raise_for_status()
            eval_run = eval_run_response.json()
            _write_json(scenario_dir / "evaluation_run.json", eval_run)
            return None
        except Exception as exc:
            tqdm.write(f"Error downloading scenario {scenario_id}: {exc}")
            return scenario_id


async def _download_tests_async(
    org_target_token: str,
    output_dir: Path,
    base_url: str,
    target_id: str,
    tests_only: bool,
    max_concurrent_requests: int,
) -> list[str]:
    async with httpx.AsyncClient() as client:
        url = f"{base_url}/v1/evaluation/targets/{target_id}/scenarios/view?limit=1000"
        response = await client.get(url, headers={"token": org_target_token})
        response.raise_for_status()
        scenarios_view = response.json()
        scenario_ids = [
            scenario["id"]
            for scenario in scenarios_view.get("evaluation_scenarios", [])
        ]

        semaphore = asyncio.Semaphore(max_concurrent_requests)
        tasks = [
            asyncio.create_task(
                _download_scenario(
                    client=client,
                    org_target_token=org_target_token,
                    output_dir=output_dir,
                    base_url=base_url,
                    target_id=target_id,
                    scenario_id=scenario_id,
                    tests_only=tests_only,
                    semaphore=semaphore,
                )
            )
            for scenario_id in scenario_ids
        ]

        error_scenarios: list[str] = []
        for task in tqdm(
            asyncio.as_completed(tasks),
            total=len(tasks),
            desc="Downloading scenarios",
            unit="scenario",
        ):
            failed_scenario = await task
            if failed_scenario:
                error_scenarios.append(failed_scenario)
        return error_scenarios


def download_tests(
    org_target_token: str,
    output_dir: Path,
    target_id: str | None = None,
    base_url: str = "https://control.neuraltrust.ai",
    tests_only: bool = False,
    max_concurrent_requests: int = 4,
) -> list[str]:
    """Download evaluation scenarios and related data locally."""
    base_url = base_url.rstrip("/")
    output_dir = Path(output_dir)
    resolved_target_id = target_id or os.getenv("NEURALTRUST_TARGET_ID")
    if not resolved_target_id:
        raise ValueError(
            "target_id is required when using the control plane API "
            "(or set NEURALTRUST_TARGET_ID)"
        )
    if max_concurrent_requests < 1:
        raise ValueError("max_concurrent_requests must be >= 1")
    return asyncio.run(
        _download_tests_async(
            org_target_token=org_target_token,
            output_dir=output_dir,
            base_url=base_url,
            target_id=resolved_target_id,
            tests_only=tests_only,
            max_concurrent_requests=max_concurrent_requests,
        )
    )


if __name__ == "__main__":
    org_target_token = ""
    target_id = "cbc0437b-319a-464e-8e78-e5e70706e8f0"
    output_dir = Path("tests")
    error_scenarios = download_tests(
        org_target_token, output_dir, target_id=target_id, max_concurrent_requests=1
    )
    print(error_scenarios)
