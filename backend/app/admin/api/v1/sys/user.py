from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, Request

from app.admin.schema.user import (
    AddUserParam,
    AvatarParam,
    GetCurrentUserInfoDetail,
    GetUserInfoListDetails,
    RegisterUserParam,
    ResetPasswordParam,
    UpdateUserParam,
    UpdateUserRoleParam,
)
from app.admin.service.user_service import user_service
from common.pagination import DependsPagination, paging_data
from common.response.response_schema import ResponseModel, response_base
from common.schema import PaginatedData
from common.security.jwt import DependsJwtAuth
from common.security.permission import RequestPermission
from common.security.rbac import DependsRBAC
from database.db_postgres import CurrentSession
from utils.serializers import select_as_dict

router = APIRouter(prefix="/user", tags=["Управление пользователями"])


@router.post(
    "/register",
    response_model=ResponseModel[None],
    summary="Зарегистрировать пользователя",
)
async def register_user(obj: RegisterUserParam) -> ResponseModel:
    await user_service.register(obj=obj)
    return response_base.success()


@router.post(
    "/add",
    response_model=ResponseModel[None],
    summary="Добавить пользователя",
    dependencies=[DependsRBAC],
)
async def add_user(request: Request, obj: AddUserParam) -> ResponseModel:
    await user_service.add(request=request, obj=obj)
    current_user = await user_service.get_userinfo(username=obj.username)
    data = GetUserInfoListDetails(**select_as_dict(current_user))
    return response_base.success(data=data)


@router.post(
    "/password/reset",
    response_model=ResponseModel[None],
    summary="Сброс пароля",
    dependencies=[DependsJwtAuth],
)
async def password_reset(request: Request, obj: ResetPasswordParam) -> ResponseModel:
    count = await user_service.pwd_reset(request=request, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.get(
    "/me",
    response_model=ResponseModel[GetCurrentUserInfoDetail],
    response_model_exclude={"password"},
    summary="Получить текущую информацию о пользователе",
    dependencies=[DependsJwtAuth],
)
async def get_current_user(request: Request) -> ResponseModel:
    data = GetCurrentUserInfoDetail(**request.user.model_dump())
    return response_base.success(data=data)


@router.get(
    "/list",
    summary="Поиск по страницам для получения информации обо всех пользователях",
    response_model=ResponseModel[PaginatedData[GetUserInfoListDetails]],
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_pagination_users(
    db: CurrentSession,
    dept: Annotated[int | None, Query()] = None,
    username: Annotated[str | None, Query()] = None,
    phone: Annotated[str | None, Query()] = None,
    status: Annotated[int | None, Query()] = None,
):
    user_select = await user_service.get_select(
        dept=dept, username=username, phone=phone, status=status
    )
    page_data = await paging_data(db, user_select, GetUserInfoListDetails)
    return response_base.success(data=page_data)


@router.get(
    "/{username}",
    response_model=ResponseModel[GetUserInfoListDetails],
    summary="Просмотр информации о пользователе",
    dependencies=[DependsJwtAuth],
)
async def get_user(username: Annotated[str, Path(...)]) -> ResponseModel:
    current_user = await user_service.get_userinfo(username=username)
    data = GetUserInfoListDetails(**select_as_dict(current_user))
    return response_base.success(data=data)


@router.put(
    "/{username}",
    summary="Обновить информацию о пользователе",
    dependencies=[DependsJwtAuth],
)
async def update_user(
    request: Request, username: Annotated[str, Path(...)], obj: UpdateUserParam
) -> ResponseModel:
    count = await user_service.update(request=request, username=username, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.put(
    "/{username}/role",
    summary="Обновить роль пользователя",
    dependencies=[
        Depends(RequestPermission("sys:user:role:edit")),
        DependsRBAC,
    ],
)
async def update_user_role(
    request: Request, username: Annotated[str, Path(...)], obj: UpdateUserRoleParam
) -> ResponseModel:
    await user_service.update_roles(request=request, username=username, obj=obj)
    return response_base.success()


@router.put(
    "/{pk}/super",
    summary="Изменить суперразрешения пользователя",
    dependencies=[DependsRBAC],
)
async def super_set(request: Request, pk: Annotated[int, Path(...)]) -> ResponseModel:
    count = await user_service.update_permission(request=request, pk=pk)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.put(
    "/{pk}/staff",
    summary="Изменить права пользователя на фоновый вход в систему",
    dependencies=[DependsRBAC],
)
async def staff_set(request: Request, pk: Annotated[int, Path(...)]) -> ResponseModel:
    count = await user_service.update_staff(request=request, pk=pk)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.put(
    "/{pk}/status", summary="Изменить статус пользователя", dependencies=[DependsRBAC]
)
async def status_set(request: Request, pk: Annotated[int, Path(...)]) -> ResponseModel:
    count = await user_service.update_status(request=request, pk=pk)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.put(
    "/{pk}/multi",
    summary="Измените статус многоточечного входа пользователя в систему",
    dependencies=[DependsRBAC],
)
async def multi_set(request: Request, pk: Annotated[int, Path(...)]) -> ResponseModel:
    count = await user_service.update_multi_login(request=request, pk=pk)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.delete(
    path="/{username}",
    summary="Выход пользователя из системы",
    description="Выйдите из системы!= Пользователь выходит из системы, после выхода из системы пользователь будет удален из базы данных",
    dependencies=[
        Depends(RequestPermission("sys:user:del")),
        DependsRBAC,
    ],
)
async def delete_user(username: Annotated[str, Path(...)]) -> ResponseModel:
    count = await user_service.delete(username=username)
    if count > 0:
        return response_base.success()
    return response_base.fail()
