import os
from typing import List

from dotenv import load_dotenv

import trusttest
from trusttest.catalog.red_team import run_red_teaming
from trusttest.language_detection.types import LanguageType
from trusttest.targets.testing import IcantAssistTarget

load_dotenv(override=True)


target = IcantAssistTarget()
client = trusttest.client(
    type="neuraltrust",
    token=os.getenv("TARGET_TOKEN"),
    target_id=os.getenv("TARGET_ID"),
)


languages: List[LanguageType] = ["English"]
for language in languages:
    run_red_teaming(
        target, language=language, client=client, num_test_cases=50, evaluate=False
    )
