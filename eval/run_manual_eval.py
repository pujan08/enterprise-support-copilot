import json
from pathlib import Path
from datetime import datetime, UTC

import requests

questions_file = Path(__file__).parent / "manual_questions.json"

with questions_file.open("r", encoding="utf-8") as f:
    questions = json.load(f)

base_url = "http://127.0.0.1:8000/ask"
TOP_K = 3
RUN_TIMESTAMP = datetime.now(UTC).isoformat()
results = []

for item in questions:
    payload = {
        "question": item["question"],
        "top": TOP_K,
    }

    try:
        response = requests.post(base_url, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        status_code = response.status_code
    except Exception as e:
        data = {
            "ok": False,
            "context_count": 0,
            "response": {
                "answer_type": "eval_request_error",
                "primary_source": None,
                "confidence": "low",
                "answer": f"Request failed: {e}",
            },
        }
        status_code = 0

    is_request_error = data.get("response", {}).get("answer_type") == "eval_request_error"

    result_item = {
        "id": item["id"],
        "question": item["question"],
        "top": payload["top"],
        "expected_has_context": item["expected_has_context"],
        "status_code": status_code,
        "ok": data.get("ok"),
        "context_count": data.get("context_count"),
        "answer_type": data.get("response", {}).get("answer_type"),
        "primary_source": data.get("response", {}).get("primary_source"),
        "confidence": data.get("response", {}).get("confidence"),
        "answer": data.get("response", {}).get("answer"),
        "passed_context_check": (
            False
            if is_request_error
            else (
                data.get("context_count", 0) > 0
                if item["expected_has_context"]
                else data.get("context_count", 0) == 0
            )
        ),
        "passed_no_filename_in_answer_check": (
            ".txt" not in (data.get("response", {}).get("answer", "") or "").lower()
            if item["expected_has_context"]
            else True
        ),
        "passed_next_steps_check": (
            len(data.get("response", {}).get("next_steps", [])) >= 2
            if item["expected_has_context"]
            else True
        ),
        "passed_answer_transition_check": (
            "recommended next steps" in (data.get("response", {}).get("answer", "") or "").lower()
            if item["expected_has_context"]
            else True
        ),
        "passed_no_context_answer_check": (
            False
            if is_request_error
            else (
                data.get("response", {}).get("answer_type") == "no_context"
                if not item["expected_has_context"]
                else True
            )
        ),
        "passed_overall": (
            False
            if is_request_error
            else (
                (
                    data.get("context_count", 0) > 0
                    if item["expected_has_context"]
                    else data.get("context_count", 0) == 0
                )
                and (
                    data.get("response", {}).get("answer_type") == "no_context"
                    if not item["expected_has_context"]
                    else True
                )
                and (
                    len(data.get("response", {}).get("next_steps", [])) >= 2
                    if item["expected_has_context"]
                    else True
                )
                and (
                    ".txt" not in (data.get("response", {}).get("answer", "") or "").lower()
                    if item["expected_has_context"]
                    else True
                )
                and (
                    "recommended next steps" in (data.get("response", {}).get("answer", "") or "").lower()
                    if item["expected_has_context"]
                    else True
                )
            )
        ),
    }

    results.append(result_item)

    print("-" * 60)
    print(f'ID: {result_item["id"]}')
    print(f'Question: {result_item["question"]}')
    print(f'Top: {result_item["top"]}')
    print(f'Status code: {result_item["status_code"]}')
    print(f'OK: {result_item["ok"]}')
    print(f'Context count: {result_item["context_count"]}')
    print(f'Answer type: {result_item["answer_type"]}')
    print(f'Primary source: {result_item["primary_source"]}')
    print(f'Confidence: {result_item["confidence"]}')
    print(f'Answer: {result_item["answer"]}')
    print(f'Passed overall: {result_item["passed_overall"]}')

total_questions = len(results)
passed_questions = sum(1 for item in results if item["passed_overall"])
failed_questions = total_questions - passed_questions
pass_rate = (passed_questions / total_questions) * 100 if total_questions else 0
request_error_count = sum(
    1 for item in results if item["answer_type"] == "eval_request_error"
)
all_checks_passed = all(item["passed_overall"] for item in results)

failed_ids = [item["id"] for item in results if not item["passed_overall"]]
failed_items = [
    {"id": item["id"], "question": item["question"]}
    for item in results
    if not item["passed_overall"]
]

output_payload = {
    "summary": {
        "run_timestamp": RUN_TIMESTAMP,
        "top_k": TOP_K,
        "total_questions": total_questions,
        "passed_questions": passed_questions,
        "failed_questions": failed_questions,
        "pass_rate": round(pass_rate, 1),
        "request_error_count": request_error_count,
        "all_checks_passed": all_checks_passed,
        "failed_ids": failed_ids,
    },
    "run_config": {
        "base_url": base_url,
        "top_k": TOP_K,
        "question_file": str(questions_file),
        "timeout_seconds": 10,
    },
    "results": results,
}

safe_timestamp = RUN_TIMESTAMP.replace(":", "-")
output_file = Path(__file__).parent / f"manual_eval_results_{safe_timestamp}.json"
output_file.write_text(json.dumps(output_payload, indent=2), encoding="utf-8")

latest_output_file = Path(__file__).parent / "manual_eval_results_latest.json"
latest_output_file.write_text(json.dumps(output_payload, indent=2), encoding="utf-8")

print("=" * 60)
print("EVAL SUMMARY")
print(f"Run timestamp: {RUN_TIMESTAMP}")
print(f"Top K: {TOP_K}")
print(f"Total questions: {total_questions}")
print(f"Passed: {passed_questions}")
print(f"Failed: {failed_questions}")
print(f"Pass rate: {pass_rate:.1f}%")
print(f"Request errors: {request_error_count}")
print(f"All checks passed: {all_checks_passed}")
print(f"Failed IDs: {failed_ids if failed_ids else 'None'}")
print(f"Failed questions: {failed_items if failed_items else 'None'}")
print(f"Saved history file: {output_file}")
print(f"Saved latest file: {latest_output_file}")