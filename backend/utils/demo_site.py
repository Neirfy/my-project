from fastapi import Request

from common.exception import errors
from core.config import settings


async def demo_site(request: Request):
    method = request.method
    path = request.url.path
    if (
        settings.DEMO_MODE
        and method != "GET"
        and method != "OPTIONS"
        and (method, path) not in settings.DEMO_MODE_EXCLUDE
    ):
        raise errors.ForbiddenError(
            msg="Эта операция запрещена в демонстрационной среде"
        )
