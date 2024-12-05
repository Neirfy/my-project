from common.model import Base, id_key
from sqlalchemy import (
    String,
    Integer,
)
from sqlalchemy.orm import Mapped, mapped_column


class Product(Base):
    __tablename__ = "sys_product"

    id: Mapped[id_key] = mapped_column(init=False)
    uuid: Mapped[str] = mapped_column(String, unique=True)
    name: Mapped[str] = mapped_column(String)
    quantity: Mapped[int] = mapped_column(Integer)
