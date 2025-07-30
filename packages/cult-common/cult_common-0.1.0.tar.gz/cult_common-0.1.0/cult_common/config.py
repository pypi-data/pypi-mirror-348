# cult_common/config.py

import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment or .env file."""

    SECRET_KEY: str = os.getenv("DJANGO_SECRET_KEY", "")
    # Kafka
    KAFKA_BOOTSTRAP_SERVERS: list[str] = (
        os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092").split(",")
    )
    KAFKA_TOPIC: str = os.getenv("KAFKA_TOPIC", "blockchain-events")
    KAFKA_GROUP_ID: str = os.getenv("KAFKA_GROUP_ID", "service-group")

    # Database
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "db")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "django")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "service_signal")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", "5432"))

    # Celery / Redis
    CELERY_BROKER_URL: str = os.getenv(
        "CELERY_BROKER_URL", "redis://redis:6379/0"
    )
    CELERY_RESULT_BACKEND: str = os.getenv(
        "CELERY_RESULT_BACKEND", "redis://redis:6379/0"
    )

    class Config:
        env_file = ".env"
        case_sensitive = True


class _SettingsProxy:
    """
    A proxy so that each attribute access does a fresh Settings() lookup —
    allowing tests to monkeypatch os.environ before reading.
    """
    def __getattr__(self, attr):
        return getattr(Settings(), attr)


# Expose `settings` exactly as before
settings = _SettingsProxy()

