from dotenv import load_dotenv
from langsmith import Client

from .langsmith_target import support_target
from .langsmith_evaluators import (
    context_relevance_evaluator,
    no_context_answer_evaluator,
    supported_answer_type_evaluator,
)

load_dotenv()

DATASET_NAME = "Enterprise Support Copilot - Retrieval Eval v1"
EXPERIMENT_PREFIX = "retrieval-eval-v1"

ls_client = Client()

results = ls_client.evaluate(
    support_target,
    data=DATASET_NAME,
    evaluators=[context_relevance_evaluator,no_context_answer_evaluator],
    experiment_prefix=EXPERIMENT_PREFIX,
    description="First formal retrieval evaluation run for Enterprise Support Copilot.",
    max_concurrency=4,
)

print("LangSmith evaluation started.")
print(results)