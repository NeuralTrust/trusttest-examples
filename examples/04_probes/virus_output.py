"""Example testing virus/malware output detection using VirusProbe and VirusEvaluator."""

from dotenv import load_dotenv

from trusttest.evaluation_scenarios import EvaluationScenario
from trusttest.evaluator_suite import EvaluatorSuite
from trusttest.evaluators import VirusEvaluator
from trusttest.probes import VirusProbe
from trusttest.targets.testing import RepeatTarget

load_dotenv(override=True)

model = RepeatTarget()

probe = VirusProbe(target=model)

scenario = EvaluationScenario(
    description="This is a test scenario",
    name="Test Scenario",
    evaluator_suite=EvaluatorSuite(
        evaluators=[VirusEvaluator()],
        criteria="any_fail",
    ),
)

test_set = probe.get_test_set()
results = scenario.evaluate(test_set)

results.display()
results.display_summary()
