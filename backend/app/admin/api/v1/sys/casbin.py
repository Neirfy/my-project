from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from app.admin.schema.casbin_rule import (
    CreatePolicyParam,
    CreateUserRoleParam,
    DeleteAllPoliciesParam,
    DeletePolicyParam,
    DeleteUserRoleParam,
    GetPolicyListDetails,
    UpdatePolicyParam,
)
from app.admin.service.casbin_service import casbin_service
from common.pagination import DependsPagination, paging_data
from common.response.response_schema import ResponseModel, response_base
from common.security.jwt import DependsJwtAuth
from common.security.permission import RequestPermission
from common.security.rbac import DependsRBAC
from database.db_postgres import CurrentSession

router = APIRouter(prefix="/casbin", tags=["Уприявление группами"])


@router.get(
    "",
    summary="Поиск по страницам для получения всех политик разрешений",
    dependencies=[
        DependsJwtAuth,
        DependsPagination,
    ],
)
async def get_pagination_casbin(
    db: CurrentSession,
    ptype: Annotated[str | None, Query(description="Тип политики, p / g")] = None,
    sub: Annotated[str | None, Query(description="uuid / роль пользователя")] = None,
) -> ResponseModel:
    casbin_select = await casbin_service.get_casbin_list(ptype=ptype, sub=sub)
    page_data = await paging_data(db, casbin_select, GetPolicyListDetails)
    return response_base.success(data=page_data)


@router.get(
    "/policies",
    summary="Получите все политики разрешений P",
    dependencies=[DependsJwtAuth],
)
async def get_all_policies(
    role: Annotated[int | None, Query(description="ID роли")] = None
) -> ResponseModel:
    policies = await casbin_service.get_policy_list(role=role)
    return response_base.success(data=policies)


@router.post(
    "/policy",
    summary="Добавить политику разрешений P",
    dependencies=[
        Depends(RequestPermission("casbin:p:add")),
        DependsRBAC,
    ],
)
async def create_policy(p: CreatePolicyParam) -> ResponseModel:
    data = await casbin_service.create_policy(p=p)
    return response_base.success(data=data)


@router.post(
    "/policies",
    summary="Добавьте несколько групп политик разрешений P",
    dependencies=[
        Depends(RequestPermission("casbin:p:group:add")),
        DependsRBAC,
    ],
)
async def create_policies(ps: list[CreatePolicyParam]) -> ResponseModel:
    data = await casbin_service.create_policies(ps=ps)
    return response_base.success(data=data)


@router.put(
    "/policy",
    summary="Обновите политику разрешений P",
    dependencies=[
        Depends(RequestPermission("casbin:p:edit")),
        DependsRBAC,
    ],
)
async def update_policy(
    old: UpdatePolicyParam, new: UpdatePolicyParam
) -> ResponseModel:
    data = await casbin_service.update_policy(old=old, new=new)
    return response_base.success(data=data)


@router.put(
    "/policies",
    summary="Обновите несколько наборов политик разрешений P",
    dependencies=[
        Depends(RequestPermission("casbin:p:group:edit")),
        DependsRBAC,
    ],
)
async def update_policies(
    old: list[UpdatePolicyParam], new: list[UpdatePolicyParam]
) -> ResponseModel:
    data = await casbin_service.update_policies(old=old, new=new)
    return response_base.success(data=data)


@router.delete(
    "/policy",
    summary="Удалить политику разрешений P",
    dependencies=[
        Depends(RequestPermission("casbin:p:del")),
        DependsRBAC,
    ],
)
async def delete_policy(p: DeletePolicyParam) -> ResponseModel:
    data = await casbin_service.delete_policy(p=p)
    return response_base.success(data=data)


@router.delete(
    "/policies",
    summary="Удаление нескольких групп политик разрешений P",
    dependencies=[
        Depends(RequestPermission("casbin:p:group:del")),
        DependsRBAC,
    ],
)
async def delete_policies(ps: list[DeletePolicyParam]) -> ResponseModel:
    data = await casbin_service.delete_policies(ps=ps)
    return response_base.success(data=data)


@router.delete(
    "/policies/all",
    summary="Удалите все политики разрешений P",
    dependencies=[
        Depends(RequestPermission("casbin:p:empty")),
        DependsRBAC,
    ],
)
async def delete_all_policies(sub: DeleteAllPoliciesParam) -> ResponseModel:
    count = await casbin_service.delete_all_policies(sub=sub)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.get(
    "/groups",
    summary="Получите все политики разрешений G",
    dependencies=[DependsJwtAuth],
)
async def get_all_groups() -> ResponseModel:
    data = await casbin_service.get_group_list()
    return response_base.success(data=data)


@router.post(
    "/group",
    summary="Добавить политику разрешений G",
    dependencies=[
        Depends(RequestPermission("casbin:g:add")),
        DependsRBAC,
    ],
)
async def create_group(g: CreateUserRoleParam) -> ResponseModel:
    data = await casbin_service.create_group(g=g)
    return response_base.success(data=data)


@router.post(
    "/groups",
    summary="Добавьте несколько групп политик общих разрешений",
    dependencies=[
        Depends(RequestPermission("casbin:g:group:add")),
        DependsRBAC,
    ],
)
async def create_groups(gs: list[CreateUserRoleParam]) -> ResponseModel:
    data = await casbin_service.create_groups(gs=gs)
    return response_base.success(data=data)


@router.delete(
    "/group",
    summary="Удалить политику разрешений G",
    dependencies=[
        Depends(RequestPermission("casbin:g:del")),
        DependsRBAC,
    ],
)
async def delete_group(g: DeleteUserRoleParam) -> ResponseModel:
    data = await casbin_service.delete_group(g=g)
    return response_base.success(data=data)


@router.delete(
    "/groups",
    summary="Удаление нескольких групп политик общих разрешений",
    dependencies=[
        Depends(RequestPermission("casbin:g:group:del")),
        DependsRBAC,
    ],
)
async def delete_groups(gs: list[DeleteUserRoleParam]) -> ResponseModel:
    data = await casbin_service.delete_groups(gs=gs)
    return response_base.success(data=data)


@router.delete(
    "/groups/all",
    summary="Удалите все политики разрешений G",
    dependencies=[
        Depends(RequestPermission("casbin:g:empty")),
        DependsRBAC,
    ],
)
async def delete_all_groups(uuid: Annotated[UUID, Query(...)]) -> ResponseModel:
    count = await casbin_service.delete_all_groups(uuid=uuid)
    if count > 0:
        return response_base.success()
    return response_base.fail()
