from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import cast
from functools import lru_cache
import os
from enum import Enum


class ENV(str, Enum):
    LOCAL = "local"
    PRODUCTION = "production"


class AppSettings(BaseSettings):
    name: str
    # -------------------------------------------------
    # Environment
    # -------------------------------------------------
    environment: ENV = Field(default=ENV.LOCAL, description="Deployment environment")
    # -------------------------------------------------
    # LLM Server
    # -------------------------------------------------
    local_url: str = Field(description="Local server URL for LLM")
    production_url: str = Field(description="Production server URL for LLM")

    # -------------------------------------------------
    # Derived
    # -------------------------------------------------
    @property
    def url(self) -> str:
        return (
            self.local_url if self.environment.value == "local" else self.production_url
        )

    # -------------------------------------------------
    # Pydantic config
    # -------------------------------------------------
    model_config = SettingsConfigDict(
        env_file="./.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


# -------------------------------------------------
# Singleton accessor
# -------------------------------------------------


@lru_cache
def get_settings() -> AppSettings:
    """Cached settings instance (safe for Streamlit/FastAPI)."""
    raw_env = os.getenv("ENV", "local")
    if raw_env not in ("local", "production"):
        raise ValueError(f"Invalid ENV value: {raw_env}")
    environment: ENV = cast(ENV, raw_env)

    return AppSettings(
        name=os.getenv("APP_NAME", "gestalt_streamlit_template"),
        environment=environment,
        local_url=os.getenv("LOCAL_URL", "http://127.0.0.1:2024"),
        production_url=os.getenv("PRODUCTION_URL", ""),
    )


if __name__ == "__main__":
    print(get_settings())
