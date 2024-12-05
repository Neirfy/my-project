from fastapi import APIRouter
from app.user.api.v1.uploader.file_hooks import router as file_router
from app.user.api.v1.bitrix_api.bitrix import router as bitrix_router

v1 = APIRouter()

v1.include_router(file_router)
v1.include_router(bitrix_router)
