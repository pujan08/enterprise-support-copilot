import os

from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition

load_dotenv()

project_endpoint = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

if not project_endpoint:
    raise ValueError("Missing AZURE_AI_PROJECT_ENDPOINT in .env")

if not deployment_name:
    raise ValueError("Missing AZURE_OPENAI_DEPLOYMENT_NAME in .env")

client = AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential(),
)

definition = PromptAgentDefinition(
    model=deployment_name,
    instructions=(
        "You are a SaaS support assistant for a support resolution copilot. "
        "Your job is to answer support questions clearly, briefly, and helpfully. "
        "Focus on login, billing, invitations, notifications, and performance issues. "
        "When appropriate, provide practical troubleshooting steps."
    ),
)

agent = client.agents.create_version(
    agent_name="support-copilot-agent",
    definition=definition,
)

print("Agent created successfully.")
print("Agent ID:", agent.id)
print("Agent Name:", getattr(agent, "name", None))
print("Model:", getattr(agent, "model", None))