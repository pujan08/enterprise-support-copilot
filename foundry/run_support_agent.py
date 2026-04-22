from foundry.support_bridge import ask_support_api


def run_support_agent(question: str, top: int = 3) -> dict:
    result = ask_support_api(question, top=top)

    return {
        "question": question,
        "answer": result["response"]["answer"],
        "next_steps": result["response"]["next_steps"],
        "confidence": result["response"]["confidence"],
        "primary_source": result["response"]["primary_source"],
    }


if __name__ == "__main__":
    output = run_support_agent("How do I log in?")

    print("Question:", output["question"])
    print("Answer:", output["answer"])
    print("Next steps:", output["next_steps"])
    print("Confidence:", output["confidence"])
    print("Primary source:", output["primary_source"])