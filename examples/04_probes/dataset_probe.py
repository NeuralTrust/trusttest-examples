"""Example using DatasetProbe with a custom dataset containing multi-language questions."""

from trusttest.dataset_builder import Dataset, DatasetItem
from trusttest.evaluation_contexts import ExpectedResponseContext
from trusttest.evaluation_scenarios import EvaluationScenario
from trusttest.evaluator_suite import EvaluatorSuite
from trusttest.evaluators import (
    CompletenessEvaluator,
    CorrectnessEvaluator,
    ToneEvaluator,
)
from trusttest.probes import DatasetProbe
from trusttest.targets.testing import DummyTarget

model = DummyTarget()

dataset = Dataset(
    [
        [
            DatasetItem(
                question="Could you share some information about the president of Spain?",
                context=ExpectedResponseContext(
                    expected_response="The president of Spain is Pedro Sánchez.",
                    question="Could you share some information about the president of Spain?",
                ),
            )
        ],
        [
            DatasetItem(
                question="Podrias hablar del presidente de Portugal?",
                context=ExpectedResponseContext(
                    expected_response="El presidente de Portugal es Marcelo Rebelo de Sousa.",
                    question="Podrias hablar del presidente de Portugal?",
                ),
            )
        ],
        [
            DatasetItem(
                question="Podries parlar del president d'Andorra?",
                context=ExpectedResponseContext(
                    expected_response="El president d'Andorra és Patrick de la Barra.",
                    question="Podries parlar del president d'Andorra?",
                ),
            )
        ],
    ]
)

probe = DatasetProbe(target=model, dataset=dataset)

test_set = probe.get_test_set()

scenario: EvaluationScenario[ExpectedResponseContext] = EvaluationScenario(
    description="This is a test scenario",
    name="Test Scenario",
    evaluator_suite=EvaluatorSuite(
        evaluators=[
            CorrectnessEvaluator(),
            CompletenessEvaluator(),
            ToneEvaluator(),
        ],
        criteria="any_fail",
    ),
)

results = scenario.evaluate(test_set)

results.display()
results.display_summary()
