from pydantic import ConfigDict, Field

from common.enums import MethodType
from common.schema import SchemaBase


class CreatePolicyParam(SchemaBase):
    sub: str = Field(..., description="uuid пользователя / id роли")
    path: str = Field(..., description="api path")
    method: MethodType = Field(default=MethodType.GET, description="Способ запроса")


class UpdatePolicyParam(CreatePolicyParam):
    pass


class DeletePolicyParam(CreatePolicyParam):
    pass


class DeleteAllPoliciesParam(SchemaBase):
    uuid: str | None = None
    role: str


class CreateUserRoleParam(SchemaBase):
    uuid: str = Field(..., description="uuid пользователя")
    role: str = Field(..., description="роль")


class DeleteUserRoleParam(CreateUserRoleParam):
    pass


class GetPolicyListDetails(SchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    ptype: str = Field(..., description="Тип правила, p / g")
    v0: str = Field(..., description="uuid / роль пользователя")
    v1: str = Field(..., description="api путь / роль")
    v2: str | None = None
    v3: str | None = None
    v4: str | None = None
    v5: str | None = None
