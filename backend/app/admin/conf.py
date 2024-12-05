from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

from core.path_conf import BasePath


# TODO
class AdminSettings(BaseSettings):
    """Admin Settings"""

    model_config = SettingsConfigDict(
        env_file=f"{BasePath}/.env", env_file_encoding="utf-8", extra="ignore"
    )

    # GitHub
    OAUTH2_GITHUB_CLIENT_ID: str
    OAUTH2_GITHUB_CLIENT_SECRET: str
    OAUTH2_GITHUB_REDIRECT_URI: str = (
        "http://127.0.0.1:8000/api/v1/oauth2/github/callback"
    )

    # Linux Do
    OAUTH2_LINUX_DO_CLIENT_ID: str
    OAUTH2_LINUX_DO_CLIENT_SECRET: str
    OAUTH2_LINUX_DO_REDIRECT_URI: str = (
        "http://127.0.0.1:8000/api/v1/oauth2/linux-do/callback"
    )

    # Front-end redirect address
    OAUTH2_FRONTEND_REDIRECT_URI: str = "http://localhost:5173/oauth2/callback"

    # Captcha
    CAPTCHA_LOGIN_REDIS_PREFIX: str = "fba:login:captcha"
    CAPTCHA_LOGIN_EXPIRE_SECONDS: int = 60 * 5

    # Config
    CONFIG_REDIS_KEY: str = "fba:config"


@lru_cache
def get_admin_settings() -> AdminSettings:
    return AdminSettings()


admin_settings = get_admin_settings()
