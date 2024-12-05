from fastapi import Depends, Request

from common.exception import errors


def get_content_type(request: Request):
    content_type = request.headers.get("Content-Type")
    if not content_type or content_type != "application/json":
        raise errors.RequestError(msg="Content-Type must be application/json")


DependsHeader = Depends(get_content_type)
