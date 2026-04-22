from dotenv import load_dotenv

from app.services import handle_ask

load_dotenv()


def support_target(inputs: dict) -> dict:
    question = inputs["question"]

    result = handle_ask(question=question, top=3)

    return {
        "ok": result.get("ok"),
        "context_count": result.get("context_count"),
        "answer_type": result.get("response", {}).get("answer_type"),
        "primary_source": result.get("response", {}).get("primary_source"),
    }