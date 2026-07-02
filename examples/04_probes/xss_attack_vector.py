"""Example testing XSS attack vector detection using XssAttackVectorProbe and XssAttackVectorEvaluator."""

from dotenv import load_dotenv

from trusttest.evaluation_scenarios import EvaluationScenario
from trusttest.evaluator_suite import EvaluatorSuite
from trusttest.evaluators import XssAttackVectorEvaluator
from trusttest.probes import XssAttackVectorProbe
from trusttest.targets.testing import IcantAssistTarget

load_dotenv(override=True)

model = IcantAssistTarget()

probe = XssAttackVectorProbe(target=model, num_test_cases=2)

scenario = EvaluationScenario(
    description="This is a test scenario",
    name="Test Scenario",
    evaluator_suite=EvaluatorSuite(
        evaluators=[XssAttackVectorEvaluator()],
        criteria="any_fail",
    ),
)

test_set = probe.get_test_set()
results = scenario.evaluate(test_set)

results.display()
results.display_summary()
