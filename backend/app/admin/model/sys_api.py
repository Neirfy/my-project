from sqlalchemy import String
from sqlalchemy.dialects.mysql import TEXT
from sqlalchemy.orm import Mapped, mapped_column

from common.model import Base, id_key


class Api(Base):
    __tablename__ = "sys_api"

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(String(50), unique=True, comment="api name")
    method: Mapped[str] = mapped_column(String(16), comment="Способ запроса")
    path: Mapped[str] = mapped_column(String(500), comment="api path")
    remark: Mapped[str | None] = mapped_column(TEXT, comment="remark")
