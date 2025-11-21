"""Example demonstrating how to save and retrieve custom evaluators from NeuralTrust."""

import os

from dotenv import load_dotenv

import trusttest
from trusttest.evaluators import (
    RegexEvaluator,
)

load_dotenv()


client = trusttest.client(type="neuraltrust", token=os.getenv("NEURALTRUST_TOKEN"))

evaluator = RegexEvaluator(pattern=r".*drugs.*")
name = "drugs 135"
description = "This evaluator checks if the response contains drugs"
client.save_evaluator(evaluator, name, description)
loaded_evaluator = client.get_evaluator(name)

print(loaded_evaluator.to_dict())
