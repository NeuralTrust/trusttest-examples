"""Example testing URL correctness evaluation with real-world test cases using UrlCorrectnessEvaluator."""

from dotenv import load_dotenv

from trusttest.evaluation_contexts import QuestionContext
from trusttest.evaluation_scenarios import EvaluationScenario
from trusttest.evaluator_suite import EvaluatorSuite
from trusttest.evaluators.llm_judges import UrlCorrectnessEvaluator
from trusttest.probes.base import Interaction, TestCase, TestSet

load_dotenv(override=True)

test_set = TestSet(
    test_cases=[
        TestCase(
            id="1",
            context={},
            interactions=[
                Interaction(
                    question="I'm interested in the ABANCA Visa Business card for my company. Can you tell me more about personalizing the card with our company's logo and what kind of payment options are available?",
                    response="""The ABANCA Visa Business card allows you to personalize it with your company's logo and background color for free if you request more than 10 cards. Payment options include monthly payments, three-month installments, or a fixed monthly fee. Learn more here: https://chat.abanca.com/y9fe0""",
                    context=QuestionContext(
                        question="I'm interested in the ABANCA Visa Business card for my company. Can you tell me more about personalizing the card with our company's logo and what kind of payment options are available?",
                    ),
                )
            ],
        ),
        TestCase(
            id="2",
            context={},
            interactions=[
                Interaction(
                    question="I need to handle some transactions in person. What are the standard business hours for commercial services at ABANCA branches?",
                    response="""ABANCA branches typically offer commercial services Monday to Friday, with extended hours Monday to Thursday by appointment. For specific hours, please check your nearest branch using this link: https://indl.io/wk7Yt.""",
                    context=QuestionContext(
                        question="I need to handle some transactions in person. What are the standard business hours for commercial services at ABANCA branches?",
                    ),
                )
            ],
        ),
        TestCase(
            id="3",
            context={},
            interactions=[
                Interaction(
                    question="Como podo cambiar a forma na que me envían a correspondencia e que debo facer para que o cambio sexa válido??",
                    response="""Para cambiar a forma de envío da correspondencia, debes notificalo por escrito á entidade. Podes facelo mediante correo postal ao domicilio social ou a través do correo electrónico buzondigital@abancaseguros.com. O cambio será válido unha vez notificado fehacientemente. Máis información en: https://chat.abanca.com/y9KmR""",
                    context=QuestionContext(
                        question="Como podo cambiar a forma na que me envían a correspondencia e que debo facer para que o cambio sexa válido??",
                    ),
                )
            ],
        ),
        TestCase(
            id="4",
            context={},
            interactions=[
                Interaction(
                    question="Could you explain the process for canceling personal data from websites and what happens if a website refuses to comply with the cancellation request??",
                    response="""To cancel personal data from websites, ABANCA Seguros Generales can request removal from specified sites. If a website refuses, options include legal claims, reporting to the Data Protection Agency, or other actions. Success may vary based on the site's country or policies. More info: https://chat.abanca.com/yeYd6""",
                    context=QuestionContext(
                        question="Could you explain the process for canceling personal data from websites and what happens if a website refuses to comply with the cancellation request??",
                    ),
                )
            ],
        ),
    ]
)

scenario = EvaluationScenario(
    name="url_correctness",
    description="Test the url correctness of the model",
    evaluator_suite=EvaluatorSuite(
        evaluators=[UrlCorrectnessEvaluator()],
    ),
)


result = scenario.evaluate(test_set)

result.display()
