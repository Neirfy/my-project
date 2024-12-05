from typing import Generic, Optional, TypeVar

from common.schema import SchemaBase

T = TypeVar("T")


class RequestErrors(SchemaBase, Generic[T]):
    code: int
    msg: str
    data: Optional[T]
    trace_id: str


class BadRequest(RequestErrors[None]):
    code: int = 400
    msg: str = "Content-Type must be application/json"


class Unauthorized(RequestErrors[None]):
    code: int = 401
    msg: str = "Token недействительный"


class ForbiddenError(RequestErrors[None]):
    code: int = 403
    msg: str = "Not authenticated"


class NotFound(RequestErrors[None]):
    code: int = 404
    msg: str = "Not Found"


class MethodNotAllowed(RequestErrors[None]):
    code: int = 405
    msg: str = "Method Not Allowed"


class InternalServerError(RequestErrors[None]):
    code: int = 500
    msg: str
