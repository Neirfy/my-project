from pathlib import Path, PosixPath
from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict
from yarl import URL
from enum import Enum


class LogLevel(str, Enum):
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    # FastAPI
    DIRECTORY: PosixPath = Path(__file__).resolve().parent.parent

    ENVIRONMENT: Literal["dev", "pro"]
    FAST_API_PORT: str
    FASTAPI_API_V1_PATH: str = "/project/v1"

    FASTAPI_TITLE: str
    FASTAPI_VERSION: str
    FASTAPI_DESCRIPTION: str
    FASTAPI_DOCS_URL: str
    FASTAPI_REDOCS_URL: str
    FASTAPI_OPENAPI_URL: str
    FASTAPI_STATIC_FILES: str

    # logs
    LOG_ROOT_LEVEL: str
    LOG_CID_DEFAULT_VALUE: str
    LOG_CID_UUID_LENGTH: int
    LOG_STDOUT_LEVEL: str
    LOG_STD_FORMAT: str
    LOG_STDERR_LEVEL: str
    LOG_STDOUT_FILENAME: str
    LOG_STDERR_FILENAME: str
    LOG_LOGURU_FORMAT: str

    # token
    TOKEN_SECRET_KEY: str
    ACCESS_TOKEN_TIME_EXPIRE: int
    ALGORITHM: str

    DATETIME_TIMEZONE: str
    DATETIME_FORMAT: str

    log_level: LogLevel = LogLevel.INFO

    # POSTGRES
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    # redis
    REDIS_HOST: str
    REDIS_USER: str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    REDIS_DATABASE: int
    REDIS_TIMEOUT: int
    REQUEST_LIMITER_REDIS_PREFIX: str

    IP_LOCATION_PARSE: Literal["online", "offline", "false"] = "offline"
    IP_LOCATION_REDIS_PREFIX: str = "fba:ip:location"
    IP_LOCATION_EXPIRE_SECONDS: int = 60 * 60 * 24 * 1

    # Token
    TOKEN_ALGORITHM: str = "HS256"
    TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 24 * 1
    TOKEN_REFRESH_EXPIRE_SECONDS: int = 60 * 60 * 24 * 7
    TOKEN_REDIS_PREFIX: str = "fba:token"
    TOKEN_REFRESH_REDIS_PREFIX: str = "fba:refresh_token"
    TOKEN_REQUEST_PATH_EXCLUDE: list[str] = [
        f"{FASTAPI_API_V1_PATH}/auth/login",
    ]

    OAUTH2_GITHUB_CLIENT_ID: str
    OAUTH2_GITHUB_CLIENT_SECRET: str
    OAUTH2_LINUX_DO_CLIENT_ID: str
    OAUTH2_LINUX_DO_CLIENT_SECRET: str

    PERMISSION_MODE: Literal["casbin", "role-menu"] = "casbin"

    PERMISSION_REDIS_PREFIX: str = "fba:permission"

    RBAC_CASBIN_EXCLUDE: set[tuple[str, str]] = {
        ("POST", f"{FASTAPI_API_V1_PATH}/auth/logout"),
        ("POST", f"{FASTAPI_API_V1_PATH}/auth/token/new"),
    }

    # Cookies
    COOKIE_REFRESH_TOKEN_KEY: str = "fba_refresh_token"
    COOKIE_REFRESH_TOKEN_EXPIRE_SECONDS: int = TOKEN_REFRESH_EXPIRE_SECONDS

    JWT_USER_REDIS_PREFIX: str = "fba:user"
    JWT_USER_REDIS_EXPIRE_SECONDS: int = 60 * 60 * 24 * 7

    DEMO_MODE: bool = False
    DEMO_MODE_EXCLUDE: set[tuple[str, str]] = {
        ("POST", f"{FASTAPI_API_V1_PATH}/auth/login"),
        ("POST", f"{FASTAPI_API_V1_PATH}/auth/logout"),
        ("GET", f"{FASTAPI_API_V1_PATH}/auth/captcha"),
    }

    RBAC_ROLE_MENU_EXCLUDE: list[str] = [
        "sys:monitor:redis",
        "sys:monitor:server",
    ]

    MIDDLEWARE_CORS: bool = True
    MIDDLEWARE_ACCESS: bool = True
    TRACE_ID_REQUEST_HEADER_KEY: str = "X-Request-ID"

    # CORS
    CORS_ALLOWED_ORIGINS: list[str] = [
        "http://localhost:8000",
    ]
    CORS_EXPOSE_HEADERS: list[str] = [
        TRACE_ID_REQUEST_HEADER_KEY,
    ]

    # birtix
    BITRIX_HOOK: str
    BITRIX_HOOK_USER: str

    ENTITY_TYPE_ID: str
    FIELD_PRODUCT: str
    FIELD_NAME: str
    FIELD_OBJECT: str
    FIELD_ADDRESS: str
    FIELD_DATE: str
    FIELD_URGENCY: str
    FIELD_COMMENT: str

    @property
    def db_url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: database URL.
        """
        return URL.build(
            scheme="postgresql+asyncpg",
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            user=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            path=f"/{self.POSTGRES_DB}",
            query={"async_fallback": "true"},
        )

    def redis_url(self, page):
        return f"redis://:{self.REDIS_PASSWORD}@wave_redis:6379/{page}"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
