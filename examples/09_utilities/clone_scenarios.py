"""Example demonstrating how to clone evaluation scenarios and test sets from NeuralTrust."""

import os
import uuid
from copy import copy

from dotenv import load_dotenv

import trusttest

load_dotenv(override=True)

app_pre_client = trusttest.client(
    type="neuraltrust", token=os.getenv("NEURALTRUST_TOKEN")
)

scenario = app_pre_client.get_evaluation_scenario(
    id="48fd648a-b1ca-407d-811b-a59bd23dbac9"
)


test_set = app_pre_client.get_evaluation_scenario_test_set(scenario.id)
eval_results = app_pre_client.get_evaluation_scenario_run(scenario.id)


new_scenario = copy(scenario)
new_scenario.id = str(uuid.uuid4())
assert new_scenario.id != scenario.id

new_test_set = copy(test_set)
new_test_set.id = str(uuid.uuid4())
assert new_test_set.id != test_set.id

for test_case in new_test_set.test_cases:
    test_case.id = str(uuid.uuid4())


app_stg_client = trusttest.client(
    type="neuraltrust", token=os.getenv("NEURALTRUST_TOKEN")
)

app_stg_client.save_evaluation_scenario(new_scenario)
app_stg_client.save_evaluation_scenario_test_set(new_scenario.id, new_test_set)
