import base64
import binascii
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _read_file(path: str) -> bytes:
    p = PROJECT_ROOT / Path(path)
    if not p.exists():
        raise RuntimeError(f"Key file not found: {p}")
    data = p.read_bytes()
    if not data:
        raise RuntimeError(f"Key file is empty: {p}")
    return data


def _decode_hmac_secret(value: str) -> bytes:
    v = value.strip()

    try:
        return base64.b64decode(v, validate=True)
    except binascii.Error:
        pass

    return v.encode("utf-8")


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
        return (
            f"postgresql+asyncpg://{self.user}:{self.password}"
            f"@{self.host}:{self.port}/{self.db}"
        )


class TelegramBotConfig(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_prefix="TELEGRAM_",
        env_file=PROJECT_ROOT / ".env",
        extra="ignore",
    )

    bot_token: str = "test"
    init_data_lifetime: int = 3600


class AccessTokenConfig(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_prefix="ACCESS_TOKEN_",
        env_file=PROJECT_ROOT / ".env",
        extra="ignore",
    )

    PRIVATE_KEY_PATH: str
    PUBLIC_KEY_PATH: str
    TTL_SECONDS: int = 3600

    private_key_pem: bytes = Field(default=b"", exclude=True)
    public_key_pem: bytes = Field(default=b"", exclude=True)

    def __init__(self, **data):
        super().__init__(**data)
        self.private_key_pem = _read_file(self.PRIVATE_KEY_PATH)
        self.public_key_pem = _read_file(self.PUBLIC_KEY_PATH)


class RefreshTokenConfig(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_prefix="REFRESH_TOKEN_",
        env_file=PROJECT_ROOT / ".env",
        extra="ignore",
    )

    HMAC_SECRET: str = "SECRET_KEY"
    TTL_SECONDS: int = 3600

    hmac_key: bytes = Field(default=b"", exclude=True)

    def __init__(self, **data):
        super().__init__(**data)
        self.hmac_key = _decode_hmac_secret(self.HMAC_SECRET)


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False, env_file=PROJECT_ROOT / ".env", env_file_encoding="utf-8"
    )

    telegram: TelegramBotConfig = Field(default_factory=TelegramBotConfig)
    postgres: PostgresConfig = Field(default_factory=PostgresConfig)
    access_token: AccessTokenConfig = Field(default_factory=AccessTokenConfig)
    refresh_token: RefreshTokenConfig = Field(default_factory=RefreshTokenConfig)


settings = AppSettings()
