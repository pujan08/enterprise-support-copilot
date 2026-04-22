from app.graph import support_graph


def print_graph_result(question: str, top: int = 3) -> None:
    result = support_graph.invoke(
        {
            "question": question,
            "top": top,
        }
    )

    final_result = result.get("result", {})
    response = final_result.get("response", {})
    raw_results = result.get("raw_search_results", [])
    filtered_results = result.get("search_results", [])

    print("=" * 60)
    print(f"Question: {question}")
    print("Has raw_search_results:", "raw_search_results" in result)
    print("Has search_results:", "search_results" in result)
    print("Has response_payload:", "response_payload" in result)
    print("Has final_ok:", "final_ok" in result)
    print("Has result:", "result" in result)
    print("Is ambiguous:", result.get("is_ambiguous"))
    print("Raw result count:", result.get("raw_result_count"))
    print("Filtered result count:", result.get("filtered_result_count"))
    print("Raw result list length:", len(raw_results))
    print("Filtered result list length:", len(filtered_results))
    print("OK:", final_result.get("ok"))
    print("Context count:", final_result.get("context_count"))
    print("Answer type:", response.get("answer_type"))
    print("Primary source:", response.get("primary_source"))
    print("Answer:", response.get("answer"))
    print("Next steps:", response.get("next_steps"))

    if raw_results:
        print("Raw top titles:", [item.get("title") for item in raw_results[:3]])
    if filtered_results:
        print("Filtered top titles:", [item.get("title") for item in filtered_results[:3]])


print_graph_result("How do I log in?")
print_graph_result("How do I change my spaceship warranty on Mars?")