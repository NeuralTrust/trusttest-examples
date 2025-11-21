"""Example testing public figures information disclosure using PublicFiguresDatasetProbe."""

import os

from dotenv import load_dotenv

from trusttest.evaluation_scenarios import EvaluationScenario
from trusttest.evaluator_suite import EvaluatorSuite
from trusttest.evaluators import TrueFalseEvaluator
from trusttest.probes.off_topic.public_figures import PublicFiguresDatasetProbe
from trusttest.targets.http import HttpTarget, PayloadConfig

load_dotenv(override=True)

model = HttpTarget(
    url="https://api.openai.com/v1/chat/completions",
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

probe = PublicFiguresDatasetProbe(
    target=model,
    max_objectives_per_category=10,
    public_figures=[
        "Elon Musk",
        "Taylor Swift",
        "Donald Trump",
        "Bill Gates",
        "Beyoncé",
    ],
)

scenario = EvaluationScenario(
    description="Test scenario for public figures information disclosure",
    name="Public Figures Test",
    evaluator_suite=EvaluatorSuite(
        evaluators=[TrueFalseEvaluator()],
        criteria="any_fail",
    ),
)

test_set = probe.get_test_set()
results = scenario.evaluate(test_set)
results.display()
results.display_summary()
