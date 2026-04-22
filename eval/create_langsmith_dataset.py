import json
from pathlib import Path

from dotenv import load_dotenv
from langsmith import Client

load_dotenv()

DATASET_NAME = "Enterprise Support Copilot - Retrieval Eval v1"

questions_file = Path(__file__).parent / "manual_questions.json"

with questions_file.open("r", encoding="utf-8") as f:
    questions = json.load(f)

examples = []

for item in questions:
    examples.append(
        {
            "inputs": {
                "question": item["question"],
            },
            "outputs": {
                "expected_has_context": item["expected_has_context"],
            },
            "metadata": {
                "id": item["id"],
            },
        }
    )

client = Client()

if client.has_dataset(dataset_name=DATASET_NAME):
    print(f"Dataset already exists: {DATASET_NAME}")
else:
    dataset = client.create_dataset(dataset_name=DATASET_NAME)
    client.create_examples(dataset_id=dataset.id, examples=examples)
    print(f"Created dataset: {DATASET_NAME}")
    print(f"Uploaded {len(examples)} examples")