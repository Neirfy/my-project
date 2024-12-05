from fastapi import APIRouter

from app.admin.api.v1.auth.auth import router as auth_router
from app.admin.api.v1.auth.captcha import router as captcha_router
from app.admin.api.v1.sys.role import router as sys_role
from app.admin.api.v1.sys.dept import router as sys_dept
from app.admin.api.v1.sys.casbin import router as sys_casbin
from app.admin.api.v1.sys.user import router as sys_router


v1 = APIRouter()

v1.include_router(auth_router)
v1.include_router(captcha_router)
v1.include_router(sys_role)
v1.include_router(sys_dept)
v1.include_router(sys_casbin)
v1.include_router(sys_router)
