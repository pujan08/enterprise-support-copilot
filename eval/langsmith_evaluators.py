def context_relevance_evaluator(run, example) -> dict:
    expected_has_context = example.outputs["expected_has_context"]
    run_output = run.outputs or {}
    actual_context_count = run_output.get("context_count", 0) or 0

    passed = (
        actual_context_count > 0
        if expected_has_context
        else actual_context_count == 0
    )

    return {
        "key": "context_relevance_check",
        "score": 1 if passed else 0,
        "comment": (
            f"expected_has_context={expected_has_context}, "
            f"context_count={actual_context_count}"
        ),
    }


def no_context_answer_evaluator(run, example) -> dict:
    expected_has_context = example.outputs["expected_has_context"]
    run_output = run.outputs or {}
    actual_answer_type = run_output.get("answer_type")

    passed = (
        True
        if expected_has_context
        else actual_answer_type == "no_context"
    )

    return {
        "key": "no_context_answer_check",
        "score": 1 if passed else 0,
        "comment": (
            f"expected_has_context={expected_has_context}, "
            f"answer_type={actual_answer_type}"
        ),
    }
def context_relevance_evaluator(run, example) -> dict:
    expected_has_context = example.outputs["expected_has_context"]
    run_output = run.outputs or {}
    actual_context_count = run_output.get("context_count", 0) or 0

    passed = (
        actual_context_count > 0
        if expected_has_context
        else actual_context_count == 0
    )

    return {
        "key": "context_relevance_check",
        "score": 1 if passed else 0,
        "comment": (
            f"expected_has_context={expected_has_context}, "
            f"context_count={actual_context_count}"
        ),
    }
def supported_answer_type_evaluator(run, example) -> dict:
    expected_has_context = example.outputs["expected_has_context"]
    run_output = run.outputs or {}
    actual_answer_type = run_output.get("answer_type")

    passed = (
        actual_answer_type == "retrieval_based_draft"
        if expected_has_context
        else True
    )

    return {
        "key": "supported_answer_type_check",
        "score": 1 if passed else 0,
        "comment": (
            f"expected_has_context={expected_has_context}, "
            f"answer_type={actual_answer_type}"
        ),
    }
def next_steps_count_evaluator(run, example) -> dict:
    expected_has_context = example.outputs["expected_has_context"]
    run_output = run.outputs or {}
    next_steps = run_output.get("next_steps", []) or []

    passed = (
        len(next_steps) >= 2
        if expected_has_context
        else True
    )

    return {
        "key": "next_steps_count_check",
        "score": 1 if passed else 0,
        "comment": (
            f"expected_has_context={expected_has_context}, "
            f"next_steps_count={len(next_steps)}"
        ),
    }
def no_filename_in_answer_evaluator(run, example) -> dict:
    expected_has_context = example.outputs["expected_has_context"]
    run_output = run.outputs or {}
    answer = (run_output.get("answer") or "").lower()

    passed = (
        ".txt" not in answer
        if expected_has_context
        else True
    )

    return {
        "key": "no_filename_in_answer_check",
        "score": 1 if passed else 0,
        "comment": (
            f"expected_has_context={expected_has_context}, "
            f"contains_txt={'.txt' in answer}"
        ),
    }
def answer_transition_evaluator(run, example) -> dict:
    expected_has_context = example.outputs["expected_has_context"]
    run_output = run.outputs or {}
    answer = (run_output.get("answer") or "").lower()

    passed = (
        "recommended next steps" in answer
        if expected_has_context
        else True
    )

    return {
        "key": "answer_transition_check",
        "score": 1 if passed else 0,
        "comment": (
            f"expected_has_context={expected_has_context}, "
            f"has_transition={'recommended next steps' in answer}"
        ),
    }