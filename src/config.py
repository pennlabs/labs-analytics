from typing import Any
from enum import Enum

from jwcrypto.jwk import JWKSet
from pydantic import PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings


class Environment(str, Enum):
    DEVELOPMENT = "DEVELOPMENT"
    TESTING = "TESTING"
    PRODUCTION = "PRODUCTION"

    @property
    def is_debug(self):
        return self in (self.DEVELOPMENT, self.TESTING)

    @property
    def is_testing(self):
        return self == self.TESTING

    @property
    def is_deployed(self) -> bool:
        return self in (self.PRODUCTION)


class Config(BaseSettings):
    DATABASE_URL: PostgresDsn
    REDIS_URL: RedisDsn
    REDIS_BATCH_SIZE: int = 1000

    JWKS_CACHE: JWKSet | None = None
    JWKS_URL: str = "https://platform.pennlabs.org/accounts/.well-known/jwks.json"

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
