#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Union

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.model import Base, id_key


class Dept(Base):
    __tablename__ = "sys_dept"

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(String(50), comment="Название отдела")
    level: Mapped[int] = mapped_column(default=0, comment="Уровень отдела")
    sort: Mapped[int] = mapped_column(default=0, comment="сортировать")
    leader: Mapped[str | None] = mapped_column(
        String(20), default=None, comment="руководитель"
    )
    phone: Mapped[str | None] = mapped_column(
        String(11), default=None, comment="телефон"
    )
    email: Mapped[str | None] = mapped_column(String(50), default=None, comment="email")
    status: Mapped[int] = mapped_column(
        default=1, comment="Статус отдела (0 отключен, 1 нормальный)"
    )
    del_flag: Mapped[bool] = mapped_column(
        default=False, comment="Флаг удаления (существует 0 для удаления 1)"
    )
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("sys_dept.id", ondelete="SET NULL"),
        default=None,
        index=True,
        comment="Идентификатор родительского отдела",
    )
    parent: Mapped[Union["Dept", None]] = relationship(
        init=False, back_populates="children", remote_side=[id]
    )
    children: Mapped[list["Dept"] | None] = relationship(
        init=False, back_populates="parent"
    )
    users: Mapped[list["User"]] = relationship(init=False, back_populates="dept")  # type: ignore
