from fastapi import Request

from common.exception.errors import ServerError
from core.config import settings


class RequestPermission:
    def __init__(self, value: str):
        self.value = value

    async def __call__(self, request: Request):
        if settings.PERMISSION_MODE == "role-menu":
            if not isinstance(self.value, str):
                raise ServerError
            request.state.permission = self.value
