from foundry.support_bridge import ask_support_api


def print_result(question: str) -> None:
    result = ask_support_api(question)

    print("=" * 60)
    print("Question:", question)
    print("Answer:", result["response"]["answer"])
    print("Next steps:", result["response"]["next_steps"])
    print("Confidence:", result["response"]["confidence"])
    print("Primary source:", result["response"]["primary_source"])


if __name__ == "__main__":
    print_result("How do I log in?")
    print_result("Why was I charged twice?")