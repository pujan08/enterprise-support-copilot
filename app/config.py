import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    app_name: str = os.getenv("APP_NAME", "Enterprise Support Resolution Copilot")
    app_env: str = os.getenv("APP_ENV", "dev")
    app_host: str = os.getenv("APP_HOST", "127.0.0.1")
    app_port: int = int(os.getenv("APP_PORT", "8000"))

    azure_search_endpoint: str = os.getenv("AZURE_SEARCH_ENDPOINT", "")
    azure_search_index_name: str = os.getenv("AZURE_SEARCH_INDEX_NAME", "")
    azure_search_api_key: str = os.getenv("AZURE_SEARCH_API_KEY", "")

    langsmith_api_key: str = os.getenv("LANGSMITH_API_KEY", "")
    langsmith_project: str = os.getenv("LANGSMITH_PROJECT", "")
    langsmith_tracing: str = os.getenv("LANGSMITH_TRACING", "false")

    foundry_agent_endpoint: str = os.getenv("FOUNDRY_AGENT_ENDPOINT", "")
    foundry_agent_api_key: str = os.getenv("FOUNDRY_AGENT_API_KEY", "")

    support_api_url: str = os.getenv("SUPPORT_API_URL", "")
    support_api_timeout_seconds: int = int(os.getenv("SUPPORT_API_TIMEOUT_SECONDS", "15"))
    azure_ai_project_endpoint: str = os.getenv("AZURE_AI_PROJECT_ENDPOINT", "")
    azure_openai_deployment_name: str = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "")

    def integration_status(self) -> dict:
        return {
            "azure_ai_search_configured": all(
                [
                    self.azure_search_endpoint,
                    self.azure_search_index_name,
                    self.azure_search_api_key,
                ]
            ),
            "langsmith_configured": bool(self.langsmith_api_key),
            "foundry_agent_configured": all(
                [
                    self.foundry_agent_endpoint,
                    self.foundry_agent_api_key,
                ]
            ),
            "support_api_configured": bool(self.support_api_url),
            "azure_ai_project_configured": all(
                [
                    self.azure_ai_project_endpoint,
                    self.azure_openai_deployment_name,
                ]
            ),
        }

    def validate_required_runtime_config(self) -> None:
        missing = []

        if not self.azure_search_endpoint:
            missing.append("AZURE_SEARCH_ENDPOINT")
        if not self.azure_search_index_name:
            missing.append("AZURE_SEARCH_INDEX_NAME")
        if not self.azure_search_api_key:
            missing.append("AZURE_SEARCH_API_KEY")

        if missing:
            raise ValueError(
                "Missing required runtime configuration: " + ", ".join(missing)
            )

        if not self.azure_search_endpoint.startswith("https://"):
            raise ValueError("AZURE_SEARCH_ENDPOINT must start with https://")

        if self.support_api_timeout_seconds <= 0:
            raise ValueError("SUPPORT_API_TIMEOUT_SECONDS must be greater than 0")


settings = Settings()
