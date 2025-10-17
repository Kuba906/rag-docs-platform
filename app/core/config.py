from pydantic import BaseModel
from os import getenv

class Settings(BaseModel):
    AZURE_OPENAI_ENDPOINT: str | None = getenv("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_API_KEY: str | None = getenv("AZURE_OPENAI_API_KEY")
    AZURE_OPENAI_DEPLOYMENT_CHAT: str = getenv("AZURE_OPENAI_DEPLOYMENT_CHAT", "gpt-4o-mini")
    AZURE_OPENAI_DEPLOYMENT_EMBED: str = getenv("AZURE_OPENAI_DEPLOYMENT_EMBED", "text-embedding-3-large")

    AZURE_SEARCH_ENDPOINT: str | None = getenv("AZURE_SEARCH_ENDPOINT")
    AZURE_SEARCH_INDEX: str = getenv("AZURE_SEARCH_INDEX", "docs")
    AZURE_SEARCH_API_KEY: str | None = getenv("AZURE_SEARCH_API_KEY")
    AZURE_SEARCH_USE_MSI: bool = getenv("AZURE_SEARCH_USE_MSI", "false").lower()=="true"

    REDIS_URL: str = getenv("REDIS_URL", "redis://redis:6379/0")
    APP_PORT: int = int(getenv("APP_PORT", "8000"))
    ALLOWED_ORIGINS: str = getenv("ALLOWED_ORIGINS", "*")
    RATE_LIMIT_RPS: int = int(getenv("RATE_LIMIT_RPS", "5"))
    DEFAULT_TENANT: str = getenv("DEFAULT_TENANT", "demo")

settings = Settings()
