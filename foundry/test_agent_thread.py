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

thread = client.agents.threads.create()

print("Thread created successfully.")
print("Thread ID:", thread.id)