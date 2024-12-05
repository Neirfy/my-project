from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query

from app.admin.schema.dept import CreateDeptParam, GetDeptListDetails, UpdateDeptParam
from app.admin.service.dept_service import dept_service
from common.response.response_schema import ResponseModel, response_base
from common.security.jwt import DependsJwtAuth
from common.security.permission import RequestPermission
from common.security.rbac import DependsRBAC
from utils.serializers import select_as_dict

router = APIRouter(prefix="/dept", tags=["Управление отделами"])


@router.get(
    "/{pk}",
    summary="Получить подробную информацию об отделе",
    dependencies=[DependsJwtAuth],
)
async def get_dept(pk: Annotated[int, Path(...)]) -> ResponseModel:
    dept = await dept_service.get(pk=pk)
    data = GetDeptListDetails(**select_as_dict(dept))
    return response_base.success(data=data)


@router.get(
    "",
    summary="Получить все отделы",
    dependencies=[DependsJwtAuth],
)
async def get_all_depts_tree(
    name: Annotated[str | None, Query()] = None,
    leader: Annotated[str | None, Query()] = None,
    phone: Annotated[str | None, Query()] = None,
    status: Annotated[int | None, Query()] = None,
) -> ResponseModel:
    dept = await dept_service.get_dept_tree(
        name=name, leader=leader, phone=phone, status=status
    )
    return response_base.success(data=dept)


@router.post(
    "",
    summary="Создать отдел",
    dependencies=[
        Depends(RequestPermission("sys:dept:add")),
        DependsRBAC,
    ],
)
async def create_dept(obj: CreateDeptParam) -> ResponseModel:
    await dept_service.create(obj=obj)
    return response_base.success()


@router.put(
    "/{pk}",
    summary="Обновить отдел",
    dependencies=[
        Depends(RequestPermission("sys:dept:edit")),
        DependsRBAC,
    ],
)
async def update_dept(
    pk: Annotated[int, Path(...)], obj: UpdateDeptParam
) -> ResponseModel:
    count = await dept_service.update(pk=pk, obj=obj)
    if count > 0:
        return response_base.success()
    return response_base.fail()


@router.delete(
    "/{pk}",
    summary="Удалить отдел",
    dependencies=[
        Depends(RequestPermission("sys:dept:del")),
        DependsRBAC,
    ],
)
async def delete_dept(pk: Annotated[int, Path(...)]) -> ResponseModel:
    count = await dept_service.delete(pk=pk)
    if count > 0:
        return response_base.success()
    return response_base.fail()
