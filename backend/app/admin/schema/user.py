from datetime import datetime

from pydantic import ConfigDict, EmailStr, Field, HttpUrl, model_validator
from typing_extensions import Self

from app.admin.schema.dept import GetDeptListDetails
from app.admin.schema.role import GetRoleListDetails
from common.enums import StatusType
from common.schema import CustomPhoneNumber, SchemaBase


class AuthSchemaBase(SchemaBase):
    username: str
    password: str | None


class AuthLoginParam(AuthSchemaBase):
    captcha: str


class RegisterUserParam(AuthSchemaBase):
    nickname: str | None = None
    fio: str
    email: EmailStr = Field(..., examples=["user@example.com"])


class AddUserParam(AuthSchemaBase):
    dept_id: int
    roles: list[int]
    nickname: str | None = None
    fio: str
    email: EmailStr = Field(..., examples=["user@example.com"])


class UserInfoSchemaBase(SchemaBase):
    dept_id: int | None = None
    username: str
    nickname: str
    fio: str
    email: EmailStr = Field(..., examples=["user@example.com"])
    phone: CustomPhoneNumber | None = None


class UpdateUserParam(UserInfoSchemaBase):
    pass


class UpdateUserRoleParam(SchemaBase):
    roles: list[int]


class AvatarParam(SchemaBase):
    url: HttpUrl = Field(..., description="HTTP-адрес аватара")


class GetUserInfoNoRelationDetail(UserInfoSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    dept_id: int | None = None
    id: int
    uuid: str
    avatar: str | None = None
    status: StatusType = Field(default=StatusType.enable)
    is_superuser: bool
    is_staff: bool
    is_multi_login: bool
    join_time: datetime = None
    last_login_time: datetime | None = None


class GetUserInfoListDetails(GetUserInfoNoRelationDetail):
    model_config = ConfigDict(from_attributes=True)
    fio: str
    is_superuser: bool

    dept: GetDeptListDetails | None = None
    roles: list[GetRoleListDetails]


class GetCurrentUserInfoDetail(GetUserInfoListDetails):
    model_config = ConfigDict(from_attributes=True)

    dept: GetDeptListDetails | str | None = None
    roles: list[GetRoleListDetails] | list[str] | None = None

    @model_validator(mode="after")
    def handel(self) -> Self:
        """Отдел обработки данных и его роль"""
        dept = self.dept
        if dept:
            self.dept = dept.name
        roles = self.roles
        if roles:
            self.roles = [role.name for role in roles]
        return self


class CurrentUserIns(GetUserInfoListDetails):
    model_config = ConfigDict(from_attributes=True)


class ResetPasswordParam(SchemaBase):
    old_password: str
    new_password: str
    confirm_password: str
