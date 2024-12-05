from fastapi import APIRouter

from core.config import settings
from app.admin.api.router import v1 as admin_v1
from app.user.api.router import v1 as user_v1


route = APIRouter(prefix=settings.FASTAPI_API_V1_PATH)

route.include_router(admin_v1)
route.include_router(user_v1)


