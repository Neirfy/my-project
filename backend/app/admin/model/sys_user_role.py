from sqlalchemy import INT, Column, ForeignKey, Integer, Table

from common.model import MappedBase

sys_user_role = Table(
    "sys_user_role",
    MappedBase.metadata,
    Column(
        "id",
        INT,
        primary_key=True,
        unique=True,
        index=True,
        autoincrement=True,
        comment="primary ID",
    ),
    Column(
        "user_id",
        Integer,
        ForeignKey("sys_user.id", ondelete="CASCADE"),
        primary_key=True,
        comment="user ID",
    ),
    Column(
        "role_id",
        Integer,
        ForeignKey("sys_role.id", ondelete="CASCADE"),
        primary_key=True,
        comment="role ID",
    ),
)
