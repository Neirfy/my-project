
from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.dialects.mysql import TEXT
from sqlalchemy.orm import Mapped, mapped_column

from common.model import DataClassBase, id_key
from utils.timezone import timezone


class LoginLog(DataClassBase):
    __tablename__ = 'sys_login_log'

    id: Mapped[id_key] = mapped_column(init=False)
    user_uuid: Mapped[str] = mapped_column(String(50), comment='UUID пользователя')
    username: Mapped[str] = mapped_column(String(20), comment='имя пользователя')
    status: Mapped[int] = mapped_column(insert_default=0, comment='Статус входа в систему (0 сбой, 1 успех)')
    ip: Mapped[str] = mapped_column(String(50), comment='IP-адрес для входа в систему')
    country: Mapped[str | None] = mapped_column(String(50), comment='Страеа')
    region: Mapped[str | None] = mapped_column(String(50), comment='Район')
    city: Mapped[str | None] = mapped_column(String(50), comment='Город')
    user_agent: Mapped[str] = mapped_column(String(255), comment='Заголовок запроса')
    os: Mapped[str | None] = mapped_column(String(50), comment='операционная система')
    browser: Mapped[str | None] = mapped_column(String(50), comment='браузер')
    device: Mapped[str | None] = mapped_column(String(50), comment='устройство')
    msg: Mapped[str] = mapped_column(TEXT, comment='Быстрое сообщение')
    login_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), comment='Время входа в систему')
    created_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), init=False, default_factory=timezone.now, comment='Время создания')