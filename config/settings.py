"""Central configuration. Endpoints come from .env; credentials come from Entra ID."""
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from azure.identity import DefaultAzureCredential


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    azure_region: str = "centralus"
    azure_resource_group: str
    storage_account_name: str
    keyvault_name: str

    ai_services_endpoint: str
    azure_openai_endpoint: str
    azure_openai_chat_deployment: str
    azure_openai_embedding_deployment: str
    azure_openai_api_version: str = "2024-10-21"
    embedding_dimensions: int = 1536

    search_endpoint: str
    search_index_name: str = "bank-policies-idx"

    applicationinsights_connection_string: str = ""

    # Retrieval tuning
    chunk_tokens: int = 700
    chunk_overlap: int = 100
    retrieval_top_k: int = 5

    @property
    def blob_endpoint(self) -> str:
        return f"https://{self.storage_account_name}.blob.core.windows.net"

    @property
    def keyvault_uri(self) -> str:
        return f"https://{self.keyvault_name}.vault.azure.net"


@lru_cache
def get_settings() -> Settings:
    return Settings()


@lru_cache
def credential() -> DefaultAzureCredential:
    """Cached. Constructing this per-call walks the whole auth chain and is slow."""
    return DefaultAzureCredential()


def token_provider():
    """Bearer token factory for the OpenAI SDK."""
    def _get() -> str:
        return credential().get_token("https://cognitiveservices.azure.com/.default").token
    return _get