from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response
from fastapi.security import HTTPBasicCredentials
from fastapi_limiter.depends import RateLimiter
from starlette.background import BackgroundTasks

from app.admin.schema.token import GetNewToken, GetSwaggerToken, GetLoginToken
from app.admin.schema.user import (
    AuthLoginParam,
    AuthSchemaBase,
)
from app.admin.service.auth_service import auth_service
from common.response.response_schema import ResponseModel, response_base
from common.security.jwt import DependsJwtAuth
from common.security.header import DependsHeader


router = APIRouter(prefix="/auth", tags=["Авторизация"])


@router.post(
    "/login/swagger",
    summary="swagger для отладки",
    description="Используется для быстрого получения токенов для аутентификации swagger",
)
async def swagger_login(
    obj: Annotated[HTTPBasicCredentials, Depends()]
) -> GetSwaggerToken:
    token, user = await auth_service.swagger_login(obj=obj)
    return GetSwaggerToken(access_token=token, user=user)


@router.post(
    "/login",
    response_model=ResponseModel[GetLoginToken],
    summary="Вход пользователя в систему",
    description="Вход в систему в формате json, поддерживается только отладка в сторонних api-инструментах, таких как: postman",
    dependencies=[DependsHeader, Depends(RateLimiter(times=5, minutes=1))],
)
async def user_login(
    request: Request,
    response: Response,
    obj: AuthSchemaBase,
    background_tasks: BackgroundTasks,
) -> ResponseModel:
    data = await auth_service.login(
        request=request, response=response, obj=obj, background_tasks=background_tasks
    )
    return response_base.success(data=data)


@router.post(
    "/login_capcha",
    summary="Вход пользователя в систему",
    description="Вход в систему в формате json, поддерживается только отладка в сторонних api-инструментах, таких как: postman",
    dependencies=[Depends(RateLimiter(times=5, minutes=1))],
)
async def user_login_capcha(
    request: Request,
    response: Response,
    obj: AuthLoginParam,
    background_tasks: BackgroundTasks,
) -> ResponseModel:
    data = await auth_service.login_capcha(
        request=request, response=response, obj=obj, background_tasks=background_tasks
    )
    return response_base.success(data=data)


@router.post(
    "/token/new",
    response_model=ResponseModel[GetNewToken],
    summary="Создание нового токена",
    dependencies=[DependsJwtAuth],
)
async def create_new_token(request: Request, response: Response) -> ResponseModel:
    data = await auth_service.new_token(request=request, response=response)
    return response_base.success(data=data)


@router.post(
    "/logout",
    response_model=ResponseModel[None],
    summary="Выход пользователя из системы",
    dependencies=[DependsJwtAuth],
)
async def user_logout(request: Request, response: Response) -> ResponseModel:
    await auth_service.logout(request=request, response=response)
    return response_base.success()
