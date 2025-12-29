from functools import lru_cache

from configs.env import settings_config
from security.cookie_policy import RefreshCookiePolicy
from security.jwt_service import JwtService


@lru_cache
def get_refresh_cookie_policy() -> RefreshCookiePolicy:
    settings = settings_config()
    return RefreshCookiePolicy(settings.security.refresh_cookie)


@lru_cache
def get_jwt_service() -> JwtService:
    settings = settings_config()
    return JwtService(settings.security.jwt)
