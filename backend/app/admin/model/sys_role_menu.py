from sqlalchemy import INT, Column, ForeignKey, Integer, Table

from common.model import MappedBase

sys_role_menu = Table(
    "sys_role_menu",
    MappedBase.metadata,
    Column(
        "id",
        INT,
        primary_key=True,
        unique=True,
        index=True,
        autoincrement=True,
        comment="ID",
    ),
    Column(
        "role_id",
        Integer,
        ForeignKey("sys_role.id", ondelete="CASCADE"),
        primary_key=True,
        comment="role ID",
    ),
    Column(
        "menu_id",
        Integer,
        ForeignKey("sys_menu.id", ondelete="CASCADE"),
        primary_key=True,
        comment="menu ID",
    ),
)
