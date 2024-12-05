from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, ForeignKey

from common.model import Base, id_key


class SmartProduct(Base):
    __tablename__ = "sys_smart_product"

    id: Mapped[id_key] = mapped_column(init=False)

    product_id: Mapped[int] = mapped_column(
        ForeignKey("sys_product.id", ondelete="CASCADE"), comment="product ID"
    )
    quantity: Mapped[int] = mapped_column(Integer, comment="product quantity")
