"""Example demonstrating how to union multiple test sets into a single test set."""

from trusttest.evaluation_contexts import ExpectedResponseContext
from trusttest.probes import TestSet

test_set_1: TestSet[ExpectedResponseContext] = TestSet.from_dict(
    {
        "test_cases": [
            {
                "interactions": [
                    {
                        "question": "What is the capital of France?",
                        "response": "Paris",
                        "context": {
                            "question": "What is the capital of France?",
                            "expected_response": "Paris",
                        },
                    }
                ],
                "context": {},
                "id": "1",
                "created_at": "2021-01-01T00:00:00Z",
            },
        ]
    }
)

test_set_2: TestSet[ExpectedResponseContext] = TestSet.from_dict(
    {
        "test_cases": [
            {
                "interactions": [
                    {
                        "question": "What is the capital of Germany?",
                        "response": "Berlin",
                        "context": {
                            "question": "What is the capital of Germany?",
                            "expected_response": "Berlin",
                        },
                    }
                ],
                "context": {},
                "id": "1",
                "created_at": "2021-01-01T00:00:00Z",
            },
        ]
    }
)

test_set_3 = TestSet.union([test_set_1, test_set_2])

print(test_set_3)
