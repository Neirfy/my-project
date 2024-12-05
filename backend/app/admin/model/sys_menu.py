from typing import Union

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.mysql import TEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.admin.model.sys_role_menu import sys_role_menu
from common.model import Base, id_key


class Menu(Base):
    __tablename__ = "sys_menu"

    id: Mapped[id_key] = mapped_column(init=False)
    title: Mapped[str] = mapped_column(String(50), comment="Название")
    name: Mapped[str] = mapped_column(String(50), comment="Название меню")
    level: Mapped[int] = mapped_column(default=0, comment="Уровень меню")
    sort: Mapped[int] = mapped_column(default=0, comment="")
    icon: Mapped[str | None] = mapped_column(
        String(100), default=None, comment="Значок меню"
    )
    path: Mapped[str | None] = mapped_column(
        String(200), default=None, comment="Адрес маршрута"
    )
    menu_type: Mapped[int] = mapped_column(
        default=0, comment="Тип меню (0 оглавлений, 1 меню, 2 кнопки)"
    )
    component: Mapped[str | None] = mapped_column(
        String(255), default=None, comment="Путь к компоненту"
    )
    perms: Mapped[str | None] = mapped_column(
        String(100), default=None, comment="Идентификатор разрешения"
    )
    status: Mapped[int] = mapped_column(
        default=1, comment="Состояние меню (0 отключено, 1 нормальное)"
    )
    show: Mapped[int] = mapped_column(
        default=1, comment="Следует ли отображать (0 нет 1 да)"
    )
    cache: Mapped[int] = mapped_column(
        default=1, comment="Нужно ли кэшировать (0 нет 1 да)"
    )
    remark: Mapped[str | None] = mapped_column(TEXT, default=None, comment="Замечания")

    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("sys_menu.id", ondelete="SET NULL"),
        default=None,
        index=True,
        comment="Идентификатор родительского меню",
    )
    parent: Mapped[Union["Menu", None]] = relationship(
        init=False, back_populates="children", remote_side=[id]
    )
    children: Mapped[list["Menu"] | None] = relationship(
        init=False, back_populates="parent"
    )
    roles: Mapped[list["Role"]] = relationship(  # type: ignore
        init=False, secondary=sys_role_menu, back_populates="menus"
    )
