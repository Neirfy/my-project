from pydantic import Field
from common.schema import SchemaBase


class ProductCreateForBitrix(SchemaBase):
    id: int
    name: str
    quantity: int


class CreateSmart(SchemaBase):
    name: str
    date: str
    urgency: bool
    object: int
    address: str
    products: list[ProductCreateForBitrix]
    comment: str


class CreateSmartProduct(SchemaBase):
    smart_id: int = Field(..., description="ID для Smart")
    product_id: int = Field(..., description="ID продукта")
    quantity: int = Field(..., description="Количество продукта")
