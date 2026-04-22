import json
from pathlib import Path

file_path = Path(__file__).parent / "manual_questions.json"

with file_path.open("r", encoding="utf-8") as f:
    questions = json.load(f)

print(f"Loaded {len(questions)} questions")

for item in questions:
    print(f'{item["id"]}: {item["question"]}')