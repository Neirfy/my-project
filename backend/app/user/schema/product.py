from typing import Optional
from pydantic import ConfigDict
from common.schema import SchemaBase


class CreateProductParam(SchemaBase):
    uuid: str
    name: str
    image: Optional[str]
    quantity: int


class GetProductInfoDetails(SchemaBase):
    id: int
    name: str
    image: Optional[str]
    quantity: int


class UpdateProductQuantityParam(SchemaBase):
    id: int
    quantity: int


class GetProductInfoListDetails(GetProductInfoDetails):
    model_config = ConfigDict(from_attributes=True)
