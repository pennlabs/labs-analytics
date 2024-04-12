from typing import Any

from jwcrypto.jwk import JWKSet
from pydantic import PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings

from .constants import Environment


class Config(BaseSettings):
    DATABASE_URL: PostgresDsn
    REDIS_URL: RedisDsn

    JWKS_CACHE: JWKSet | None = None
    JWKS_URL: str = "https://platform.pennlabs.org/identity/jwks/"

    SITE_DOMAIN: str = "analytics.pennlabs.org"

    ENVIRONMENT: Environment = Environment.PRODUCTION

    CORS_ORIGINS: list[str] = ["*"]
    CORS_ORIGINS_REGEX: str | None = None
    CORS_HEADERS: list[str] = ["*"]

    APP_VERSION: str = "1"


settings = Config()

app_configs: dict[str, Any] = {
    "title": "Labs Analytics API",
    "root_path": "",
}
if settings.ENVIRONMENT.is_deployed:
    app_configs["root_path"] = f"/v{settings.APP_VERSION}"

if not settings.ENVIRONMENT.is_debug:
    app_configs["openapi_url"] = None  # hide docs
