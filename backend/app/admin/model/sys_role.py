from sqlalchemy import String
from sqlalchemy.dialects.mysql import TEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.admin.model.sys_role_menu import sys_role_menu
from app.admin.model.sys_user_role import sys_user_role
from common.model import Base, id_key


class Role(Base):
    __tablename__ = "sys_role"

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(
        String(20), unique=True, comment="Имя пользователя"
    )
    data_scope: Mapped[int | None] = mapped_column(
        default=2,
        comment="бъем полномочий (1: Права доступа ко всем данным 2: Пользовательские права доступа к данным)",
    )
    status: Mapped[int] = mapped_column(
        default=1, comment="Статус персонажа (0 отключен, 1 нормальный)"
    )
    remark: Mapped[str | None] = mapped_column(TEXT, default=None, comment="Замечания")

    users: Mapped[list["User"]] = relationship(  # type: ignore
        init=False, secondary=sys_user_role, back_populates="roles"
    )
    menus: Mapped[list["Menu"]] = relationship(  # type: ignore
        init=False, secondary=sys_role_menu, back_populates="roles"
    )
