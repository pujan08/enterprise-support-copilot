import json
from pathlib import Path

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

print(f"Prepared {len(examples)} dataset examples")

for example in examples[:3]:
    print(example)