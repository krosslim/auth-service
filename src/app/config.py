from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[2]


class PostgresConfig(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_prefix="POSTGRES_",
        env_file=PROJECT_ROOT / ".env",
        extra="ignore",
    )

    host: str = "localhost"
    port: int = 5432
    user: str = "postgres"
    password: str = "postgres"
    db: str = "postgres"
    pool_size: int = 1
    pool_timeout: int = 1
    pool_pre_ping: bool = True
    pool_recycle: int = 3600
    max_overflow: int = 1
    echo: bool = False

    @property
    def dsn(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


class TelegramBotConfig(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_prefix="TELEGRAM_",
        env_file=PROJECT_ROOT / ".env",
        extra="ignore",
    )

    bot_token: str = "test"
    init_data_lifetime: int = 3600


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False, env_file=PROJECT_ROOT / ".env", env_file_encoding="utf-8"
    )

    telegram: TelegramBotConfig = Field(default_factory=TelegramBotConfig)
    postgres: PostgresConfig = Field(default_factory=PostgresConfig)


settings = AppSettings()
