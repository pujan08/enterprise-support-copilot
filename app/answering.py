from langsmith import traceable


def extract_possible_causes(snippet: str) -> list[str]:
    marker = "Possible causes include"

    if marker not in snippet:
        return []

    causes_text = snippet.split(marker, 1)[1].strip().rstrip(".")
    return [cause.strip() for cause in causes_text.split(" or ") if cause.strip()]


def build_next_steps(causes: list[str]) -> list[str]:
    steps = []

    if "password reset issues" in causes:
        steps.append("Ask the customer to try a password reset.")

    if "browser cache problems" in causes:
        steps.append("Ask the customer to clear their browser cache and try again.")

    return steps


def classify_confidence(
    context: list[dict],
    causes: list[str] | None = None,
    next_steps: list[str] | None = None,
) -> str:
    if not context:
        return "low"

    causes = causes or []
    next_steps = next_steps or []

    top_score = context[0].get("score", 0) or 0
    second_score = context[1].get("score", 0) or 0 if len(context) > 1 else 0
    score_gap = top_score - second_score
    context_count = len(context)

    has_actionable_steps = len(next_steps) >= 2
    has_specific_signal = bool(causes)

    if (
        top_score >= 1.5
        and score_gap >= 0.5
        and context_count == 1
        and has_actionable_steps
    ):
        return "high"

    if (
        top_score >= 0.8
        and (has_actionable_steps or has_specific_signal)
    ):
        return "medium"

    return "low"


def extract_recommended_steps(content: str, max_steps: int = 3) -> list[str]:
    if not content:
        return []

    steps = []
    lines = content.splitlines()

    # First pass: numbered troubleshooting steps
    for line in lines:
        clean_line = line.strip()

        if not clean_line:
            continue

        if clean_line[:2] in {"1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9."}:
            step_text = clean_line[2:].strip()
            if step_text:
                steps.append(step_text)

        if len(steps) >= max_steps:
            return steps[:max_steps]

    # Second pass: FAQ-style answers
    for line in lines:
        clean_line = line.strip()

        if not clean_line:
            continue

        if clean_line.startswith("A:"):
            answer_text = clean_line[2:].strip()

            if not answer_text:
                continue

            sentences = [s.strip() for s in answer_text.split(".") if s.strip()]

            for sentence in sentences:
                normalized = sentence[0].upper() + sentence[1:] if len(sentence) > 1 else sentence.upper()

                if not normalized.endswith("."):
                    normalized += "."

                steps.append(normalized)

                if len(steps) >= max_steps:
                    return steps[:max_steps]

    return steps[:max_steps]

def describe_source_title(title: str) -> str:
    normalized = (title or "").strip().lower()

    if normalized == "login-account-access-support.txt":
        return "a login or account access problem"
    if normalized == "billing-support.txt":
        return "a billing or subscription problem"
    if normalized == "invitations-permissions-support.txt":
        return "a user invitation or permissions problem"
    if normalized == "notifications-email-delivery-support.txt":
        return "a notification or email delivery problem"
    if normalized == "performance-slow-loading-support.txt":
        return "a performance or slow loading problem"
    if normalized == "login-faq.txt":
        return "a login or account access problem"
    if normalized == "billing-faq.txt":
        return "a billing or subscription problem"
    if normalized == "invitations-permissions-faq.txt":
        return "a user invitation or permissions problem"
    if normalized == "notifications-email-faq.txt":
        return "a notification or email delivery problem"
    if normalized == "performance-faq.txt":
        return "a performance or slow loading problem"

    return "a support problem covered in the knowledge base"


@traceable(
    name="build_draft_answer",
    tags=["support-answering"],
    metadata={"component": "answering"},
)
def build_draft_answer(question: str, context: list[dict]) -> dict:
    top_item = context[0]
    snippet = top_item.get("snippet", "")
    full_content = top_item.get("content", "") or ""
    title = top_item.get("title", "Unknown source")
    causes = extract_possible_causes(snippet)

    next_steps = extract_recommended_steps(full_content)
    confidence = classify_confidence(context, causes=causes, next_steps=next_steps)

    if causes:
        answer = (
            "The most likely causes are: "
            + ", ".join(causes)
            + ". The recommended next steps are below."
        )
    else:
        answer = (
            "This appears to be "
            + describe_source_title(title)
            + ". The recommended next steps are below."
        )

    if not next_steps:
        next_steps = ["Review the linked support source for more details."]

    return {
        "answer": answer,
        "answer_type": "retrieval_based_draft",
        "next_steps": next_steps,
        "sources": [
            {
                "title": item.get("title"),
                "id": item.get("id"),
                "score": item.get("score"),
            }
            for item in context
        ],
        "primary_source": title,
        "confidence": confidence,
    }