from datetime import datetime

from pydantic import ConfigDict, Field

from common.enums import StatusType
from common.schema import CustomEmailStr, CustomPhoneNumber, SchemaBase


class DeptSchemaBase(SchemaBase):
    name: str
    parent_id: int | None = Field(
        default=None, description="Идентификатор родителя отдела"
    )
    sort: int = Field(default=0, ge=0, description="сортировать")
    leader: str | None = None
    phone: CustomPhoneNumber | None = None
    email: CustomEmailStr | None = None
    status: StatusType = Field(default=StatusType.enable)


class CreateDeptParam(DeptSchemaBase):
    pass


class UpdateDeptParam(DeptSchemaBase):
    pass


class GetDeptListDetails(DeptSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    del_flag: bool
    created_time: datetime
    updated_time: datetime | None = None
