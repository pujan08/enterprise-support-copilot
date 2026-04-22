import os

from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

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

print("Foundry project client created successfully.")
print("Endpoint:", project_endpoint)
print("Deployment name:", deployment_name)