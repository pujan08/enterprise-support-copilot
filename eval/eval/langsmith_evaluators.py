def context_relevance_evaluator(run_output: dict, reference_output: dict) -> dict:
    expected_has_context = reference_output["expected_has_context"]
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