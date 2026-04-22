import os

from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

load_dotenv()

project_endpoint = os.getenv("AZURE_AI_PROJECT_ENDPOINT")

if not project_endpoint:
    raise ValueError("Missing AZURE_AI_PROJECT_ENDPOINT in .env")

client = AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential(),
)

with client.get_openai_client() as openai_client:
    conversation = openai_client.conversations.create(
        items=[
            {
                "type": "message",
                "role": "user",
                "content": "How do I log in?",
            }
        ]
    )

    print("Conversation created successfully.")
    print("Conversation ID:", conversation.id)

    response = openai_client.responses.create(
    conversation=conversation.id,
    extra_body={
        "agent_reference": {
            "name": "support-copilot-agent",
            "type": "agent_reference",
        }
    },
    )

    print("Response created successfully.")
    for item in response.output:
        if item.type == "message":
            for content in item.content:
                if content.type == "output_text":
                    print("Assistant reply:")
                    print(content.text)