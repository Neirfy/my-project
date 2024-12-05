from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, Request

from app.admin.schema.role import (
    CreateRoleParam,
    GetRoleListDetails,
    UpdateRoleMenuParam,
    UpdateRoleParam,
)
from app.admin.service.menu_service import menu_service
from app.admin.service.role_service import role_service
from common.pagination import DependsPagination, paging_data
from common.response.response_schema import ResponseModel, response_base
from common.security.jwt import DependsJwtAuth
from common.security.permission import RequestPermission
from common.security.rbac import DependsRBAC
from database.db_postgres import CurrentSession
from utils.serializers import select_as_dict, select_list_serialize

router = APIRouter(prefix="/role", tags=["Управление ролью"])


@router.get("/all", summary="Получить все роли", dependencies=[DependsJwtAuth])
async def get_all_roles() -> ResponseModel:
    roles = await role_service.get_all()
    data = select_list_serialize(roles)
    return response_base.success(data=data)


@router.get(
    "/{pk}/all",
    summary="Получить все роли пользователей",
    dependencies=[DependsJwtAuth],
)
async def get_user_all_roles(pk: Annotated[int, Path(...)]) -> ResponseModel:
    roles = await role_service.get_user_roles(pk=pk)
    data = select_list_serialize(roles)
    return response_base.success(data=data)


@router.get(
    "/{pk}/menus",
    summary="Получить доступ ко всем меню пользователя",
    dependencies=[DependsJwtAuth],
)
async def get_role_all_menus(pk: Annotated[int, Path(...)]) -> ResponseModel:
    menu = await menu_service.get_role_menu_tree(pk=pk)
    return response_base.success(data=menu)


@router.get(
    "/{pk}",
    summary="Получить подробную информацию о роли",
    dependencies=[DependsJwtAuth],
)
async def get_role(pk: Annotated[int, Path(...)]) -> ResponseModel:
    role = await role_service.get(pk=pk)
    data = GetRoleListDetails(**select_as_dict(role))
    return response_base.success(data=data)


@router.get(
    "",
    summary="Поиск по страницам для получения всех ролей",
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_pagination_roles(
    db: CurrentSession,
    name: Annotated[str | None, Query()] = None,
    data_scope: Annotated[int | None, Query()] = None,
    status: Annotated[int | None, Query()] = None,
) -> ResponseModel:
    role_select = await role_service.get_select(
        name=name, data_scope=data_scope, status=status
    )
    page_data = await paging_data(db, role_select, GetRoleListDetails)
    return response_base.success(data=page_data)


@router.post(
    "",
    summary="Создание роли",
    dependencies=[
        Depends(RequestPermission("sys:role:add")),
        DependsRBAC,
    ],
)
async def create_role(obj: CreateRoleParam) -> ResponseModel:
    await role_service.create(obj=obj)
    return response_base.success()


@router.put(
    "/{pk}",
    summary="Обновление роли",
    dependencies=[
        Depends(RequestPermission("sys:role:edit")),
        DependsRBAC,
    ],
)
async def update_role(
    pk: Annotated[int, Path(...)], obj: UpdateRoleParam
) -> ResponseModel:
    count = await role_service.update(pk=pk, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.put(
    "/{pk}/menu",
    summary="Обновите меню ролей",
    dependencies=[
        Depends(RequestPermission("sys:role:menu:edit")),
        DependsRBAC,
    ],
)
async def update_role_menus(
    request: Request, pk: Annotated[int, Path(...)], menu_ids: UpdateRoleMenuParam
) -> ResponseModel:
    count = await role_service.update_role_menu(
        request=request, pk=pk, menu_ids=menu_ids
    )
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.delete(
    "",
    summary="Удаление ролей",
    dependencies=[
        Depends(RequestPermission("sys:role:del")),
        DependsRBAC,
    ],
)
async def delete_role(pk: Annotated[list[int], Query(...)]) -> ResponseModel:
    count = await role_service.delete(pk=pk)
    if count > 0:
        return response_base.success()
    return response_base.fail()
