from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

import trusttest
from trusttest.clients.base import Client
from trusttest.evaluation_scenarios.base import EvaluationRun, EvaluationScenario
from trusttest.probes.base import TestSet

load_dotenv(override=True)

SCENARIO_FILENAME: str = "evaluation_scenario.json"
TEST_SET_FILENAME: str = "test_set.json"


def main() -> None:
    """Command-line entrypoint."""
    parser: argparse.ArgumentParser = _build_argument_parser()
    args: argparse.Namespace = parser.parse_args()
    runs: list[EvaluationRun[Any]] = evaluate_and_upload_all(
        root_folder=args.folder,
        token=args.token,
        target_id=args.target_id,
    )
    print(f"Completed {len(runs)} scenarios.")


def _build_argument_parser() -> argparse.ArgumentParser:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description=(
            "Recursively evaluate scenario folders with local JSON files and upload "
            "scenario, test-set, and run results."
        )
    )
    parser.add_argument(
        "folder",
        type=str,
        help="Root folder containing scenario directories.",
    )
    parser.add_argument(
        "token",
        type=str,
        help="NeuralTrust target token used to upload results.",
    )
    parser.add_argument(
        "target_id",
        type=str,
        help="NeuralTrust target ID used to upload results.",
    )
    return parser


def evaluate_and_upload_all(
    root_folder: str | Path, token: str, target_id: str
) -> list[EvaluationRun[Any]]:
    """Evaluate and upload all scenarios found recursively.

    Args:
        root_folder: Folder to scan for scenarios.
        token: NeuralTrust target token used for uploads.
        target_id: NeuralTrust target ID used for uploads.

    Returns:
        Evaluation runs for all successfully processed scenarios.

    Raises:
        RuntimeError: If at least one scenario fails to process.
    """
    scenario_dirs: list[Path] = find_scenario_dirs(root_folder)
    if not scenario_dirs:
        print(f"No scenario folders found in {Path(root_folder).resolve()}")
        return []

    client: Client = trusttest.client(
        type="neuraltrust", token=token, target_id=target_id
    )
    runs: list[EvaluationRun[Any]] = []

    print(f"Found {len(scenario_dirs)} scenario folders.")
    for index, scenario_dir in enumerate(scenario_dirs, start=1):
        print(f"[{index}/{len(scenario_dirs)}] Processing {scenario_dir}")
        try:
            scenario: EvaluationScenario[Any]
            test_set: TestSet[Any]
            scenario, test_set = load_scenario_and_test_set(scenario_dir=scenario_dir)
            evaluation_run: EvaluationRun[Any] = scenario.evaluate(test_set)

            client.save_evaluation_scenario(scenario)
            client.save_evaluation_scenario_test_set(scenario.id, test_set)
            client.save_evaluation_scenario_run(evaluation_run)
            runs.append(evaluation_run)
            print(
                f"Uploaded run for scenario '{evaluation_run.scenario_name}' ({evaluation_run.scenario_id})."
            )
        except Exception as exc:
            print(f"Failed to process {scenario_dir}: {exc}")

    return runs


def find_scenario_dirs(root_folder: str | Path) -> list[Path]:
    """Find scenario directories recursively from a root folder.

    A scenario directory is any directory that contains both
    `evaluation_scenario.json` and `test_set.json`.

    Args:
        root_folder: Base folder to search recursively.

    Returns:
        A sorted list of scenario directory paths.

    Raises:
        FileNotFoundError: If the root folder does not exist.
        NotADirectoryError: If the root path is not a directory.
    """
    root_path: Path = Path(root_folder).expanduser().resolve()
    if not root_path.exists():
        raise FileNotFoundError(f"Root folder does not exist: {root_path}")
    if not root_path.is_dir():
        raise NotADirectoryError(f"Root path is not a directory: {root_path}")

    scenario_dirs: set[Path] = set()
    for scenario_file in root_path.rglob(SCENARIO_FILENAME):
        scenario_dir: Path = scenario_file.parent
        test_set_path: Path = scenario_dir / TEST_SET_FILENAME
        if test_set_path.is_file():
            scenario_dirs.add(scenario_dir)

    return sorted(scenario_dirs)


def load_scenario_and_test_set(
    scenario_dir: Path,
) -> tuple[EvaluationScenario[Any], TestSet[Any]]:
    """Load one scenario and test set from JSON files.

    Args:
        scenario_dir: Directory containing scenario files.

    Returns:
        A tuple with loaded `EvaluationScenario` and `TestSet`.
    """
    scenario_path: Path = scenario_dir / SCENARIO_FILENAME
    test_set_path: Path = scenario_dir / TEST_SET_FILENAME

    with scenario_path.open("r", encoding="utf-8") as scenario_file:
        scenario_data: dict[str, Any] = json.load(scenario_file)
    with test_set_path.open("r", encoding="utf-8") as test_set_file:
        test_set_data: dict[str, Any] = json.load(test_set_file)

    scenario: EvaluationScenario[Any] = EvaluationScenario.from_dict(scenario_data)
    test_set: TestSet[Any] = TestSet.from_dict(test_set_data)
    return scenario, test_set


if __name__ == "__main__":
    main()
