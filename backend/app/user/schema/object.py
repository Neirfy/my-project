from pydantic import BaseModel
from pydantic import ConfigDict, Field

from common.schema import SchemaBase


class CreateObjectParam(SchemaBase):
    id: int
    name: str
    address: str


class UpdateObjectParam(SchemaBase):
    name: str
    address: str


class GetObjectInfoDetails(SchemaBase):
    id: int
    name: str
    address: str


class GetObjectInfoListDetails(GetObjectInfoDetails):
    model_config = ConfigDict(from_attributes=True)
