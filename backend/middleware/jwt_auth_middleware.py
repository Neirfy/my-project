from typing import Any

from fastapi import Request, Response
from fastapi.security.utils import get_authorization_scheme_param
from pydantic_core import from_json
from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    AuthenticationError,
)
from starlette.requests import HTTPConnection

from app.admin.schema.user import CurrentUserIns
from common.exception.errors import TokenError
from common.logger import logger
from common.security import jwt
from core.config import settings
from database.db_postgres import async_session
from database.db_redis import redis_client
from utils.serializers import MsgSpecJSONResponse, select_as_dict


class _AuthenticationError(AuthenticationError):
    def __init__(
        self,
        *,
        code: int = None,
        msg: str = None,
        headers: dict[str, Any] | None = None,
    ):
        self.code = code
        self.msg = msg
        self.headers = headers


class JwtAuthMiddleware(AuthenticationBackend):
    """JWT Промежуточное программное обеспечение для аутентификации"""

    @staticmethod
    def auth_exception_handler(
        conn: HTTPConnection, exc: _AuthenticationError
    ) -> Response:
        """Рассмотрим обработку ошибок внутренней аутентификации"""
        return MsgSpecJSONResponse(
            content={"code": exc.code, "msg": exc.msg, "data": None},
            status_code=exc.code,
        )

    async def authenticate(
        self, request: Request
    ) -> tuple[AuthCredentials, CurrentUserIns] | None:
        token = request.headers.get("Authorization")
        if not token:
            return

        if request.url.path in settings.TOKEN_REQUEST_PATH_EXCLUDE:
            return

        scheme, token = get_authorization_scheme_param(token)
        if scheme.lower() != "bearer":
            return

        try:
            sub = await jwt.jwt_authentication(token)
            cache_user = await redis_client.get(
                f"{settings.JWT_USER_REDIS_PREFIX}:{sub}"
            )
            # print(cache_user)
            if not cache_user:
                async with async_session() as db:
                    current_user = await jwt.get_current_user(db, sub)
                    user = CurrentUserIns(**select_as_dict(current_user))
                    await redis_client.setex(
                        f"{settings.JWT_USER_REDIS_PREFIX}:{sub}",
                        settings.JWT_USER_REDIS_EXPIRE_SECONDS,
                        user.model_dump_json(),
                    )
            else:
                user = CurrentUserIns.model_validate(
                    from_json(cache_user, allow_partial=True)
                )
        except TokenError as exc:
            raise _AuthenticationError(
                code=exc.code, msg=exc.detail, headers=exc.headers
            )
        except Exception as e:
            logger.error(f"JWT :{e}")
            raise _AuthenticationError(
                code=getattr(e, "code", 500),
                msg=getattr(e, "msg", "Internal Server Error"),
            )

        return AuthCredentials(["authenticated"]), user
