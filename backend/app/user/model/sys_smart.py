from sqlalchemy import (
    Boolean,
    ForeignKey,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column
from common.model import Base, id_key


class Smart(Base):
    __tablename__ = "sys_smart"

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    date: Mapped[str] = mapped_column(String, nullable=False)
    urgency: Mapped[bool] = mapped_column(Boolean, default=False)
    comment: Mapped[str] = mapped_column(String, default=None)

    object_id: Mapped[int | None] = mapped_column(
        ForeignKey("sys_object.id", ondelete="SET NULL"),
        default=None,
        comment="ID, связанный с Объектом",
    )
