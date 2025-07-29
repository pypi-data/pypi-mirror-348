from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn

class PostgresSettings(BaseSettings):
    """Postgres settings for the application."""

    # Database connection settings
    db_url: PostgresDsn

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        env_prefix="POSTGRES_"
    )