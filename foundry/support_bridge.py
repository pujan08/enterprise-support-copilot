import os

import requests
from dotenv import load_dotenv

load_dotenv()

SUPPORT_API_URL = os.getenv("SUPPORT_API_URL")
SUPPORT_API_TIMEOUT_SECONDS = int(os.getenv("SUPPORT_API_TIMEOUT_SECONDS", "15"))

if not SUPPORT_API_URL:
    raise ValueError("Missing SUPPORT_API_URL in .env")


def ask_support_api(question: str, top: int = 3) -> dict:
    payload = {
        "question": question,
        "top": top,
    }

    try:
        response = requests.post(
            SUPPORT_API_URL,
            json=payload,
            timeout=SUPPORT_API_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {
            "ok": False,
            "response": {
                "answer": f"Support API request failed: {e}",
                "answer_type": "bridge_error",
                "next_steps": [
                    "Check whether the support API is running and reachable.",
                    "Verify SUPPORT_API_URL in the environment configuration.",
                ],
                "confidence": "low",
                "primary_source": None,
            },
        }