from dotenv import load_dotenv
from trusttest.catalog.red_team import run_red_teaming
from trusttest.clients.file_system import FileSystemClient
from trusttest.language_detection.types import LanguageType
from trusttest.targets.testing import IcantAssistTarget

load_dotenv(override=True)


target = IcantAssistTarget()
client = FileSystemClient(path="trusttest_db")


languages: list[LanguageType] = ["English"]
for language in languages:
    run_red_teaming(
        target, language=language, client=client, num_test_cases=50, evaluate=False
    )


print(client.get_overview())
