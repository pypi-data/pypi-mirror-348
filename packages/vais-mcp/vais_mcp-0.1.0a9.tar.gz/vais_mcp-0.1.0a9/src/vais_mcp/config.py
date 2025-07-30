from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    GOOGLE_CLOUD_PROJECT_ID: str
    IMPERSONATE_SERVICE_ACCOUNT: Optional[str] = None
    SOURCE_SA_KEY_PATH: Optional[str] = "/app/secrets/sa-key.json"

    VAIS_ENGINE_ID: str
    VAIS_LOCATION: str = "global"
    PAGE_SIZE: int = 5
    MAX_EXTRACTIVE_SEGMENT_COUNT: int = 2

    LOG_LEVEL: str = "WARNING"

    model_config = SettingsConfigDict(extra="ignore", env_ignore_empty=True)


# Auto-validation of required fields
settings = Settings()
