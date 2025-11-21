"""Example demonstrating custom evaluator creation using CustomEvaluatorExpected with detailed scoring criteria."""

import os

from dotenv import load_dotenv

import trusttest
from trusttest.dataset_builder import Dataset
from trusttest.evaluation_contexts import ExpectedResponseContext
from trusttest.evaluation_scenarios import EvaluationScenario
from trusttest.evaluator_suite import EvaluatorSuite
from trusttest.evaluators import CustomEvaluatorExpected
from trusttest.probes import DatasetProbe
from trusttest.targets.testing import DummyTarget

load_dotenv()

client = trusttest.client(type="neuraltrust", token=os.getenv("NEURALTRUST_TOKEN"))

dataset_path = "examples/data/qa_dataset.json"
dataset: Dataset[ExpectedResponseContext] = Dataset.from_json(path=dataset_path)
probe = DatasetProbe(target=DummyTarget(), dataset=dataset)


evaluator = CustomEvaluatorExpected(
    name="Trip Plan Accuracy",
    description="Validates that the trip plan (including flights, itinerary, and activities) matches the user's request and is logically consistent. Avoids assumptions about the year unless explicitly stated by the user.",
    instructions="""
    **Instruction:** Evaluate the accuracy and completeness of the trip plan in the actual response against the user's prompt/question. Verify the following:
    1. **Flights:** Ensure the flight details (origin, destination, departure/return dates, city descriptions) are correct and match the user's request. Do not assume the year unless explicitly stated by the user. If there is no currently available flight, the response is still correct.
    2. **Itinerary:** Confirm that the daily activities and destinations align with the user's intended trip (e.g., trip destination, place).
    3. **Logical Consistency:** Check that the trip plan is feasible (e.g., travel times between locations, logical sequence of activities).
    4. **Relevance:** Ensure the trip plan is relevant to the user's request (e.g., place, time, days, zone).

    Deduct points for:
    - Missing or incorrect flight details.
    - Inaccurate or irrelevant activities in the itinerary.
    - Infeasible or illogical trip plans.
    - Lack of alignment with the user's request.
    - Incorrect assumptions about the year (e.g., assuming 2024 instead of 2025).
    """,
    threshold=3,
    score_range=(1, 5),
    scores=[
        {
            "score": 1,
            "description": "The trip plan is entirely incorrect or irrelevant to the user's request. Flights and itinerary are missing or completely mismatched..",
        },
        {
            "score": 2,
            "description": "The trip plan is mostly incorrect or irrelevant. Major inaccuracies in flights, itinerary, or logical consistency.",
        },
        {
            "score": 3,
            "description": "The trip plan includes some correct elements but has multiple inaccuracies (e.g., incorrect dates, irrelevant activities, or illogical sequencing).",
        },
        {
            "score": 4,
            "description": "The trip plan matches the user's request with only minor inaccuracies (e.g., a single incorrect date or a minor activity mismatch)..",
        },
        {
            "score": 5,
            "description": "The trip plan exactly matches the user's request, with correct flights, a logical and relevant itinerary, and no inaccuracies.",
        },
    ],
)


scenario = EvaluationScenario(
    description="This is a test scenario",
    name="Test Scenario",
    evaluator_suite=EvaluatorSuite(
        evaluators=[evaluator],
        criteria="all_fail",
    ),
)


test_set = probe.get_test_set()
results = scenario.evaluate(test_set)

client.save_evaluation_scenario(scenario)
client.save_evaluation_scenario_test_set(scenario.id, test_set)
client.save_evaluation_scenario_run(results)


loaded_scenario = client.get_evaluation_scenario(scenario.id)
results = loaded_scenario.evaluate(test_set)

results.display_summary()
