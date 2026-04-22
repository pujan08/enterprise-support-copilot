from app.search import run_search
from app.answering import build_draft_answer
from langsmith import traceable
from langsmith import get_current_run_tree

def has_minimum_relevance(question: str, context: list[dict]) -> bool:
    if not context:
        return False

    top_result = context[0]
    normalized_question = question.strip().lower()
    top_text = f'{top_result.get("title", "")} {top_result.get("snippet", "")}'.lower()

    support_themes = {
        "auth": [
            "login",
            "log in",
            "sign in",
            "password",
            "reset",
            "cache",
            "account",
            "session",
            "browser",
        ],
        "billing": [
            "billing",
            "invoice",
            "payment",
            "subscription",
            "charge",
            "charged",
            "refund",
            "cancel",
            "renew",
            "trial",
            "plan",
        ],
        "invite": [
            "invite",
            "invitation",
            "permission",
            "role",
            "access",
            "workspace",
            "team",
            "teammate",
            "admin",
            "member",
        ],
        "notifications": [
            "email",
            "notification",
            "notifications",
            "verification",
            "reminder",
            "digest",
            "alert",
            "alerts",
            "spam",
            "junk",
        ],
        "performance": [
            "slow",
            "loading",
            "load",
            "dashboard",
            "freeze",
            "freezing",
            "lag",
            "timeout",
            "spinning",
            "browser",
            "refresh loop",
           
        ],
    }

    matched_themes = []

    for theme_name, keywords in support_themes.items():
        if any(keyword in normalized_question for keyword in keywords):
            matched_themes.append(theme_name)

    if not matched_themes:
        return False

    for theme_name in matched_themes:
        keywords = support_themes[theme_name]
        if any(keyword in top_text for keyword in keywords):
            return True

    return False

def build_no_context_response(question: str, top: int) -> dict:
    return {
        "ok": False,
        "question": question,
        "top": top,
        "context_count": 0,
        "response": {
            "answer": "I could not find relevant support content for this question.",
            "answer_type": "no_context",
            "next_steps": [
                "Try rephrasing the question or checking whether the knowledge base contains this topic."
            ],
            "sources": [],
            "primary_source": None,
            "confidence": "low",
        },
    }

def build_success_response(question: str, top: int, context: list[dict]) -> dict:
    draft_answer = build_draft_answer(question, context)

    return {
        "ok": True,
        "question": question,
        "top": top,
        "context_count": len(context),
        "response": draft_answer,
    }

@traceable(name="support_question_flow", tags=["support-api"], metadata={"component": "services"})
def handle_ask(question: str, top: int = 3) -> dict:
    if not question.strip():
        return {
            "ok": False,
            "question": question,
            "top": top,
            "context_count": 0,
            "response": {
                "answer": "The question cannot be empty.",
                "answer_type": "invalid_input",
                "next_steps": ["Enter a support question before submitting the request."],
                "sources": [],
                "primary_source": None,
                "confidence": "low",
            },
        }

    search_response = run_search(question, top=top)
    context = search_response.get("results", [])
    if not has_minimum_relevance(question, context):
        context = [item for item in context if has_minimum_relevance(question, [item])]

    rt = get_current_run_tree()
    if rt is not None:
        rt.metadata["context_count"] = len(context)

    if not context:
        rt = get_current_run_tree()
        if rt is not None:
            rt.metadata["answer_type"] = "no_context"
        return build_no_context_response(question, top)

    rt = get_current_run_tree()
    if rt is not None:
        rt.metadata["answer_type"] = "retrieval_based_draft"

    return build_success_response(question, top, context)