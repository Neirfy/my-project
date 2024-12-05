from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from common.model import Base


class Object(Base):
    __tablename__ = "sys_object"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(String)
    address: Mapped[str] = mapped_column(String)
