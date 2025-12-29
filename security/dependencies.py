from collections.abc import Callable
from typing import Any
from fastapi import Depends, Request

from core.exceptions.auth_exceptions import TokenExpiredException, AuthTokenMissingException, InvalidTokenException, \
    ForbiddenException
from security.principals import CurrentUser


def get_token_claims(request: Request) -> dict[str, Any] | None:
    """
    Lấy claims từ TokenContextMiddleware
    Middleware đã decode sẵn vào request.state.token_claims
    """
    return getattr(request.state, "token_claims", None)


def get_token_error(request: Request) -> str | None:
    """
    token_error: None | "expired" | "invalid" (được set từ middleware). :contentReference[oaicite:8]{index=8}
    """
    return getattr(request.state, "token_error", None)


def require_current_user(
        request: Request,
) -> CurrentUser:
    """
    Dependency bắt buộc khi đăng nhập
    - Không có token -> 401 (missing)
    - Token expired/invalid -> 401
    - Có claims -> build CurrentUser

    Dùng cho endpoint ít nhạy cảm / nội bộ / access token TTL ngắn
    """
    err = get_token_error(request)
    if err == "expired":
        raise TokenExpiredException(token_type="access")
    if err == "invalid":
        raise InvalidTokenException(token_type="access")

    claims = get_token_claims(request)
    if not claims:
        raise AuthTokenMissingException(token_type="access")

    return CurrentUser.from_claims(claims)


def require_permissions(*required: str) -> Callable[[CurrentUser], CurrentUser]:
    """
    Factory dependency: require_permissions("student:read", "student:write")
    - Nếu thiếu bất kỳ permission nào -> 403
    """
    required_set = set(required)

    def _dep(user: CurrentUser = Depends(require_current_user)) -> CurrentUser:
        # Các permission được yêu cầu nhưng user không có
        # dùng toán tử '-' với set
        missing = sorted(required_set - user.permissions)

        if missing:
            raise ForbiddenException(required=missing)
        return user

    return _dep


def require_roles(*required: str) -> Callable[[CurrentUser], CurrentUser]:
    """
    Factory dependency: require_roles("admin", "manager")
    - Nếu user không có bất kỳ role nào trong required -> 403
    """
    required_set = set(required)

    def _dep(user: CurrentUser = Depends(require_current_user)) -> CurrentUser:
        user_roles = set(user.roles)

        # Các role được yêu cầu nhưng user không có
        missing = sorted(required_set - user_roles)

        if len(missing) == len(required_set):
            # user không có role nào trong required
            raise ForbiddenException(required=[f"role:{r}" for r in missing])

        return user

    return _dep
