import os
import time
from typing import List

import requests
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv(override=True)


EXECUTED_SCENARIO_IDS: List[str] = []

token = os.environ["TARGET_TOKEN"]
target_id = ""
base_url = "https://control.neuraltrust.ai"

target_base = f"{base_url}/v1/evaluation/targets/{target_id}"

all_scenarios = requests.get(
    f"{target_base}/scenarios/view?limit=1000",
    headers={"Authorization": f"Bearer {token}"},
)
all_scenarios.raise_for_status()
all_scenarios = all_scenarios.json()

scenario_ids = []
for scenario in all_scenarios["evaluation_scenarios"]:
    scenario_ids.append(scenario["id"])

error_scenarios = []
final_scenarios = [
    scenario for scenario in scenario_ids if scenario not in EXECUTED_SCENARIO_IDS
]

for scenario_id in tqdm(final_scenarios):
    print(f"Running scenario {scenario_id}")
    try:
        run_response = requests.post(
            f"{target_base}/scenarios/{scenario_id}/execute",
            headers={"Authorization": f"Bearer {token}"},
        )
        run_response.raise_for_status()
        print(run_response.json())
        time.sleep(240)
    except Exception as e:
        error_scenarios.append(scenario_id)
        print(e)

print(error_scenarios)
