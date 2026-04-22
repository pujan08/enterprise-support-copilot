import requests


def ask_support_api(question: str, top: int = 3) -> dict:
    payload = {
        "question": question,
        "top": top,
    }

    response = requests.post(
        "http://127.0.0.1:8000/ask",
        json=payload,
        timeout=15,
    )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    result = ask_support_api("Why was I charged twice?")

    print("Bridge worked.")
    print("Answer:", result["response"]["answer"])
    print("Next steps:", result["response"]["next_steps"])
    print("Confidence:", result["response"]["confidence"])
    print("Primary source:", result["response"]["primary_source"])