from enum import Enum
from enum import IntEnum as SourceIntEnum
from typing import Type


class _EnumBase:
    @classmethod
    def get_member_keys(cls: Type[Enum]) -> list[str]:
        return [name for name in cls.__members__.keys()]

    @classmethod
    def get_member_values(cls: Type[Enum]) -> list:
        return [item.value for item in cls.__members__.values()]


class IntEnum(_EnumBase, SourceIntEnum):
    pass


class StrEnum(_EnumBase, str, Enum):
    pass


class MenuType(IntEnum):
    directory = 0
    menu = 1
    button = 2


class RoleDataScopeType(IntEnum):
    all = 1
    custom = 2


class MethodType(StrEnum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    OPTIONS = "OPTIONS"


class LoginLogStatusType(IntEnum):
    fail = 0
    success = 1


class BuildTreeType(StrEnum):
    traversal = "traversal"
    recursive = "recursive"


class OperaLogCipherType(IntEnum):
    aes = 0
    md5 = 1
    itsdangerous = 2
    plan = 3


class StatusType(IntEnum):
    disable = 0
    enable = 1


class UserSocialType(StrEnum):
    github = "GitHub"
    linuxdo = "LinuxDo"
