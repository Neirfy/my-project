from sqlalchemy import String
from sqlalchemy.dialects.mysql import TEXT
from sqlalchemy.orm import Mapped, mapped_column

from common.model import MappedBase, id_key


class CasbinRule(MappedBase):
    __tablename__ = "sys_casbin_rule"

    id: Mapped[id_key]
    ptype: Mapped[str] = mapped_column(String(255), comment="Тип политики: p / g")
    v0: Mapped[str] = mapped_column(
        String(255), comment="Идентификатор роли / uuid пользователя"
    )
    v1: Mapped[str] = mapped_column(TEXT, comment="путь к api / имя роли")
    v2: Mapped[str | None] = mapped_column(String(255), comment="Способ запроса")
    v3: Mapped[str | None] = mapped_column(String(255))
    v4: Mapped[str | None] = mapped_column(String(255))
    v5: Mapped[str | None] = mapped_column(String(255))

    def __str__(self):
        arr = [self.ptype]
        for v in (self.v0, self.v1, self.v2, self.v3, self.v4, self.v5):
            if v is None:
                break
            arr.append(v)
        return ", ".join(arr)

    def __repr__(self):
        return '<CasbinRule {}: "{}">'.format(self.id, str(self))
