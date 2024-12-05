from math import ceil

from fastapi import FastAPI, Request, Response
from fastapi.routing import APIRoute

from common.exception import errors


def ensure_unique_route_names(app: FastAPI) -> None:
    """
    Проверьте, является ли название маршрута уникальным

    :param app:
    :return:
    """
    temp_routes = set()
    for route in app.routes:
        # print(route)
        if isinstance(route, APIRoute):
            if route.name in temp_routes:
                raise ValueError(f'Non-unique route name: {route.name}')
            temp_routes.add(route.name)


async def http_limit_callback(request: Request, response: Response, expire: int):
    """
    Функция обратного вызова по умолчанию при запросе ограничения

    :param request:
    :param response:
    :param expire: Оставшиеся миллисекунды
    :return:
    """
    expires = ceil(expire / 1000)
    raise errors.HTTPError(code=429, msg='Запрос выполняется слишком часто, пожалуйста, повторите попытку позже', headers={'Retry-After': str(expires)})