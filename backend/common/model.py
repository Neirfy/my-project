from datetime import datetime
from typing import Annotated

from sqlalchemy import DateTime
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    MappedAsDataclass,
    declared_attr,
    mapped_column,
)

from utils.timezone import timezone

id_key = Annotated[
    int,
    mapped_column(
        primary_key=True,
        index=True,
        autoincrement=True,
        sort_order=-999,
        comment="Идентификатор первичного ключа",
    ),
]


class UserMixin(MappedAsDataclass):
    """Пользовательский mixin"""

    create_user: Mapped[int] = mapped_column(sort_order=998, comment="Дата создания")
    update_user: Mapped[int | None] = mapped_column(
        init=False, default=None, sort_order=998, comment="Дата обновления"
    )


class DateTimeMixin(MappedAsDataclass):
    """Класс данных для mixin даты и времени"""

    created_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        init=False,
        default_factory=timezone.now,
        sort_order=999,
        comment="Время создания",
    )
    updated_time: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        init=False,
        onupdate=timezone.now,
        sort_order=999,
        comment="Время обновления",
    )


class MappedBase(DeclarativeBase):
    """
    Декларативный базовый класс, исходный класс DeclarativeBase,
    существует как родительский класс всех базовых классов или классов моделей данных
    """

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class DataClassBase(MappedAsDataclass, MappedBase):
    """
    Декларативный класс данных базовый класс
    """

    __abstract__ = True


class Base(DataClassBase, DateTimeMixin):

    __abstract__ = True
