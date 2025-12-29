from functools import lru_cache
from typing import Any

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, SecretStr

from configs.settings.security import SecuritySettings, SameSite, JwtSettings, JwtAlgorithm, RefreshCookieSettings


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    environment: str = Field(..., validation_alias="ENVIRONMENT")
    database_url: str = Field(..., validation_alias="DATABASE_URL")

    cors_allow_origins_raw: str | None = Field(default=None, validation_alias="CORS_ALLOW_ORIGINS")
    jwt_algorithm: JwtAlgorithm = Field(default="HS256", validation_alias="JWT_ALGORITHM")
    jwt_secret_key: SecretStr = Field(..., validation_alias="JWT_SECRET_KEY")
    jwt_issuer: str = Field(..., validation_alias="JWT_ISSUER")
    jwt_audience: str = Field(..., validation_alias="JWT_AUDIENCE")
    access_token_expired_minutes: int = Field(default=15, validation_alias="ACCESS_TOKEN_EXPIRED_MINUTES")
    refresh_token_expired_minutes: int = Field(default=20160, validation_alias="REFRESH_SESSION_TTL_MINUTES")
    refresh_cookie_secure: bool | None = Field(default=None, validation_alias="REFRESH_COOKIE_SECURE")
    refresh_cookie_samesite: SameSite | None = Field(default=None, validation_alias="REFRESH_COOKIE_SAMESITE")
    refresh_cookie_path: str | None = Field(default=None, validation_alias="REFRESH_COOKIE_PATH")
    refresh_cookie_max_age_seconds: int | None = Field(default=None, validation_alias="REFRESH_COOKIE_MAX_AGE_SECONDS")

    security: SecuritySettings = Field(default_factory=SecuritySettings)

    tz: str = Field(default="UTC", validation_alias="TZ")

    pool_size: int = Field(default=10, validation_alias="DB_POOL_SIZE")
    max_overflow: int = Field(default=20, validation_alias="DB_MAX_OVERFLOW")

    # Pydantic hook để mapping CORS origins, JWT, refresh session TTL, refresh cookie settings
    def model_post_init(self, __context):
        updates: dict[str, Any] = {}

        updates.update(self._build_cors_updates())
        updates.update(self._build_jwt_updates())
        updates.update(self._build_refresh_session_updates())
        updates.update(self._build_refresh_cookie_updates())  # có validate cross-field

        # Apply once
        if updates:
            self.security = self.security.model_copy(update=updates)

    # Builders nội dung update
    def _build_cors_updates(self) -> dict[str, Any]:
        if not self.cors_allow_origins_raw:
            return {}

        origins = [o.strip() for o in self.cors_allow_origins_raw.split(",") if o.strip()]
        return {"cors": self.security.cors.model_copy(update={"allow_origins": origins})}

    def _build_jwt_updates(self) -> dict[str, Any]:
        issuer = (self.jwt_issuer or "").strip()
        audience = (self.jwt_audience or "").strip()
        secret = self.jwt_secret_key.get_secret_value().strip()

        if not issuer:
            raise ValueError("Invalid JWT config: JWT_ISSUER must not be empty")
        if not audience:
            raise ValueError("Invalid JWT config: JWT_AUDIENCE must not be empty")
        if not secret:
            raise ValueError("Invalid JWT config: JWT_SECRET_KEY must not be empty")
        if self.access_token_expired_minutes <= 0:
            raise ValueError("Invalid JWT config: ACCESS_TOKEN_EXPIRED_MINUTES must be > 0")

        jwt_settings = JwtSettings(
            algorithm=self.jwt_algorithm,
            secret_key=self.jwt_secret_key,
            issuer=issuer,
            audience=audience,
            access_token_ttl_minutes=self.access_token_expired_minutes,
        )
        return {"jwt": jwt_settings}

    def _build_refresh_session_updates(self) -> dict[str, Any]:
        if self.refresh_token_expired_minutes <= 0:
            raise ValueError("Invalid refresh session config: REFRESH_SESSION_TTL_MINUTES must be > 0")

        refresh_session = self.security.refresh_session.model_copy(
            update={"ttl_minutes": self.refresh_token_expired_minutes}
        )
        return {"refresh_session": refresh_session}

    def _build_refresh_cookie_updates(self) -> dict[str, Any]:
        cookie_settings = self._merge_refresh_cookie_settings()
        self._validate_cookie_policy(cookie_settings)
        return {"refresh_cookie": cookie_settings}

    def _merge_refresh_cookie_settings(self) -> RefreshCookieSettings:
        refresh_updates: dict[str, Any] = {}

        if self.refresh_cookie_secure is not None:
            refresh_updates["secure"] = self.refresh_cookie_secure
        if self.refresh_cookie_samesite is not None:
            refresh_updates["samesite"] = self.refresh_cookie_samesite
        if self.refresh_cookie_path:
            refresh_updates["path"] = self.refresh_cookie_path.strip()
        if self.refresh_cookie_max_age_seconds is not None:
            if self.refresh_cookie_max_age_seconds <= 0:
                raise ValueError("Invalid cookie config: REFRESH_COOKIE_MAX_AGE_SECONDS must be > 0")
            refresh_updates["max_age_seconds"] = self.refresh_cookie_max_age_seconds

        return (
            self.security.refresh_cookie.model_copy(update=refresh_updates)
            if refresh_updates
            else self.security.refresh_cookie
        )

    @staticmethod
    def _validate_cookie_policy(cookie_settings: RefreshCookieSettings) -> None:
        if cookie_settings.samesite == "none" and cookie_settings.secure is not True:
            raise ValueError("Invalid cookie policy: SameSite=None requires Secure=true")


@lru_cache
def settings_config() -> Settings:
    # noinspection PyArgumentList
    return Settings()
