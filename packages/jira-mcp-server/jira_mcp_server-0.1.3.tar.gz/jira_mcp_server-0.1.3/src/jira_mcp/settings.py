from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class JiraSettings(BaseSettings):
    """Loads Jira configuration from environment variables or .env file."""
    model_config = SettingsConfigDict(
        env_prefix="JIRA_",
        env_file=".env",
        extra="ignore",
    )

    base_url: AnyHttpUrl = Field(..., description="URL of the Jira instance (e.g., https://yourjira.com)")
    username: str | None = Field(None, description="Jira username for basic authentication")
    password: str | None = Field(None, description="Jira password or API token for basic authentication")
    session_id: str | None = Field(None, description="Jira JSESSIONID cookie value for session authentication")

    @property
    def has_basic_auth(self) -> bool:
        return bool(self.username and self.password)

    @property
    def has_session_auth(self) -> bool:
        return bool(self.session_id)

# Create a single instance to be used across the application
settings = JiraSettings()

# Perform a check at import time to ensure some form of auth is configured
if not settings.has_basic_auth and not settings.has_session_auth:
    raise ValueError(
        "Jira authentication not configured. "
        "Please set JIRA_SESSION_ID or both JIRA_USERNAME and JIRA_PASSWORD "
        "in your environment or .env file."
    )

if not settings.base_url:
     raise ValueError("JIRA_BASE_URL must be configured.")