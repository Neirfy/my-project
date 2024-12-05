from datetime import datetime
from typing import Union

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.admin.model.sys_user_role import sys_user_role
from common.model import Base, id_key
from database.db_postgres import uuid4_str
from utils.timezone import timezone


class User(Base):
    __tablename__ = "sys_user"

    id: Mapped[id_key] = mapped_column(init=False)
    uuid: Mapped[str] = mapped_column(
        String(50), init=False, default_factory=uuid4_str, unique=True
    )
    username: Mapped[str] = mapped_column(
        String(20), unique=True, index=True, comment="имя пользователя"
    )
    fio: Mapped[str] = mapped_column(String)
    nickname: Mapped[str] = mapped_column(String(20), unique=True, comment="прозвище")
    password: Mapped[str | None] = mapped_column(String(255), comment="Пароль")
    salt: Mapped[str | None] = mapped_column(String(5), comment="Соль")
    email: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, comment="email"
    )
    is_superuser: Mapped[bool] = mapped_column(
        default=False, comment="Высший авторитет (0 нет 1 да)"
    )
    is_staff: Mapped[bool] = mapped_column(
        default=False, comment="Вход в систему для фонового управления (0 нет 1 да)"
    )
    status: Mapped[int] = mapped_column(
        default=1,
        comment="Статус учетной записи пользователя (0 отключен, 1 нормальный)",
    )
    is_multi_login: Mapped[bool] = mapped_column(
        default=False, comment="ледует ли повторно входить в систему (0 нет 1 да)"
    )
    avatar: Mapped[str | None] = mapped_column(
        String(255), default=None, comment="Аватар"
    )
    phone: Mapped[str | None] = mapped_column(
        String(11), default=None, comment="Номер телефона"
    )

    join_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        init=False,
        default_factory=timezone.now,
        comment="Время регистрации",
    )
    last_login_time: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        init=False,
        onupdate=timezone.now,
        comment="Последний вход в систему",
    )

    dept_id: Mapped[int | None] = mapped_column(
        ForeignKey("sys_dept.id", ondelete="SET NULL"),
        default=None,
        comment="ID, связанный с отделом",
    )
    dept: Mapped[Union["Dept", None]] = relationship(  # type: ignore
        init=False, back_populates="users"
    )

    roles: Mapped[list["Role"]] = relationship(  # type: ignore
        init=False, secondary=sys_user_role, back_populates="users"
    )
