from typing import TypedDict, NotRequired

from langgraph.graph import StateGraph, START, END

from app.search import run_search
from app.answering import build_draft_answer
from app.services import build_no_context_response, has_minimum_relevance


class SupportGraphState(TypedDict):
    question: str
    top: NotRequired[int]
    raw_search_results: NotRequired[list[dict]]
    search_results: NotRequired[list[dict]]
    raw_result_count: NotRequired[int]
    filtered_result_count: NotRequired[int]
    is_ambiguous: NotRequired[bool]
    response_payload: NotRequired[dict]
    final_ok: NotRequired[bool]
    result: NotRequired[dict]


def search_documents_node(state: SupportGraphState) -> dict:
    question = state["question"]
    top = state.get("top", 3)

    search_response = run_search(question, top=top)
    raw_results = search_response.get("results", [])

    return {
        "raw_search_results": raw_results,
        "raw_result_count": len(raw_results),
    }


def filter_relevant_context_node(state: SupportGraphState) -> dict:
    question = state["question"]
    raw_results = state.get("raw_search_results", [])

    filtered_results = [
        item for item in raw_results if has_minimum_relevance(question, [item])
    ]

    return {
        "search_results": filtered_results,
        "filtered_result_count": len(filtered_results),
        "is_ambiguous": len(filtered_results) > 1,
    }


def route_after_filtering(state: SupportGraphState) -> str:
    filtered_count = state.get("filtered_result_count", 0)
    is_ambiguous = state.get("is_ambiguous", False)

    if filtered_count == 0:
        return "build_no_context"

    if is_ambiguous:
        return "build_answer_then_annotate"

    return "build_answer"


def build_answer_node(state: SupportGraphState) -> dict:
    question = state["question"]
    context = state.get("search_results", [])

    draft_answer = build_draft_answer(question, context)

    return {
        "response_payload": draft_answer,
        "final_ok": True,
    }


def annotate_ambiguous_answer_node(state: SupportGraphState) -> dict:
    response_payload = dict(state.get("response_payload", {}) or {})

    next_steps = response_payload.get("next_steps", []) or []
    next_steps.append(
        "Check the linked support sources if the first recommendation does not match your exact issue."
    )
    response_payload["next_steps"] = next_steps

    if response_payload.get("confidence") == "high":
        response_payload["confidence"] = "medium"

    return {
        "response_payload": response_payload,
    }


def build_no_context_node(state: SupportGraphState) -> dict:
    question = state["question"]
    top = state.get("top", 3)

    no_context_result = build_no_context_response(question, top)

    return {
        "response_payload": no_context_result["response"],
        "final_ok": no_context_result["ok"],
    }


def prepare_final_response_node(state: SupportGraphState) -> dict:
    question = state["question"]
    top = state.get("top", 3)
    context = state.get("search_results", [])
    response_payload = state.get("response_payload", {})
    final_ok = state.get("final_ok", False)

    result = {
        "ok": final_ok,
        "question": question,
        "top": top,
        "context_count": len(context),
        "response": response_payload,
    }

    return {"result": result}


graph_builder = StateGraph(SupportGraphState)
graph_builder.add_node("search_documents", search_documents_node)
graph_builder.add_node("filter_relevant_context", filter_relevant_context_node)
graph_builder.add_node("build_answer", build_answer_node)
graph_builder.add_node("annotate_ambiguous_answer", annotate_ambiguous_answer_node)
graph_builder.add_node("build_no_context", build_no_context_node)
graph_builder.add_node("prepare_final_response", prepare_final_response_node)

graph_builder.add_edge(START, "search_documents")
graph_builder.add_edge("search_documents", "filter_relevant_context")
graph_builder.add_conditional_edges(
    "filter_relevant_context",
    route_after_filtering,
    {
        "build_answer": "build_answer",
        "build_answer_then_annotate": "build_answer",
        "build_no_context": "build_no_context",
    },
)
graph_builder.add_edge("build_answer", "prepare_final_response")
graph_builder.add_edge("build_no_context", "prepare_final_response")
graph_builder.add_edge("annotate_ambiguous_answer", "prepare_final_response")

graph_builder.add_conditional_edges(
    "build_answer",
    lambda state: "annotate_ambiguous_answer" if state.get("is_ambiguous", False) else "prepare_final_response",
    {
        "annotate_ambiguous_answer": "annotate_ambiguous_answer",
        "prepare_final_response": "prepare_final_response",
    },
)

graph_builder.add_edge("prepare_final_response", END)

support_graph = graph_builder.compile()