from datetime import datetime

from pydantic import ConfigDict, Field

from app.admin.schema.menu import GetMenuListDetails
from common.enums import RoleDataScopeType, StatusType
from common.schema import SchemaBase


class RoleSchemaBase(SchemaBase):
    name: str
    data_scope: RoleDataScopeType = Field(
        default=RoleDataScopeType.custom,
        description="Объем полномочий (1: Разрешения на все данные; 2: Пользовательские разрешения на данные)",
    )
    status: StatusType = Field(default=StatusType.enable)
    remark: str | None = None


class CreateRoleParam(RoleSchemaBase):
    pass


class UpdateRoleParam(RoleSchemaBase):
    pass


class UpdateRoleMenuParam(SchemaBase):
    menus: list[int]


class GetRoleListDetails(RoleSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_time: datetime
    updated_time: datetime | None = None
    menus: list[GetMenuListDetails]
