from contextlib import asynccontextmanager

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import Depends, FastAPI
from fastapi_limiter import FastAPILimiter
from fastapi_pagination import add_pagination
from starlette.middleware.authentication import AuthenticationMiddleware

from app.router import route
from common.exception.exception_handler import register_exception
from common.logger import set_customize_logfile, setup_logging
from core.config import settings
from core.path_conf import STATIC_DIR
from database.db_postgres import create_table
from database.db_redis import redis_client
from middleware.jwt_auth_middleware import JwtAuthMiddleware
from middleware.state_middleware import StateMiddleware
from utils.demo_site import demo_site
from utils.health_check import ensure_unique_route_names, http_limit_callback
from utils.openapi import simplify_operation_ids
from utils.serializers import MsgSpecJSONResponse
from middleware.access_middleware import AccessMiddleware


@asynccontextmanager
async def register_init(app: FastAPI):

    await create_table()
    await redis_client.open()
    await FastAPILimiter.init(
        redis=redis_client,
        prefix=settings.REQUEST_LIMITER_REDIS_PREFIX,
        http_callback=http_limit_callback,
    )

    yield

    await redis_client.close()
    await FastAPILimiter.close()


def register_app():
    # FastAPI
    app = FastAPI(
        title=settings.FASTAPI_TITLE,
        version=settings.FASTAPI_VERSION,
        description=settings.FASTAPI_DESCRIPTION,
        docs_url=settings.FASTAPI_DOCS_URL,
        redoc_url=settings.FASTAPI_REDOCS_URL,
        openapi_url=settings.FASTAPI_OPENAPI_URL,
        default_response_class=MsgSpecJSONResponse,
        lifespan=register_init,
    )

    register_logger()

    register_static_file(app)

    register_middleware(app)

    register_router(app)

    register_page(app)

    register_exception(app)

    return app


def register_logger() -> None:
    setup_logging()
    set_customize_logfile()


def register_static_file(app: FastAPI):
    """
    :param app:
    :return:
    """
    if settings.FASTAPI_STATIC_FILES:
        import os

        from fastapi.staticfiles import StaticFiles

        if not os.path.exists(STATIC_DIR):
            os.mkdir(STATIC_DIR)
        app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


def register_middleware(app: FastAPI):
    app.add_middleware(
        AuthenticationMiddleware,
        backend=JwtAuthMiddleware(),
        on_error=JwtAuthMiddleware.auth_exception_handler,
    )
    if settings.MIDDLEWARE_ACCESS:
        app.add_middleware(AccessMiddleware)
    app.add_middleware(StateMiddleware)
    app.add_middleware(CorrelationIdMiddleware, validator=False)
    if settings.MIDDLEWARE_CORS:
        from fastapi.middleware.cors import CORSMiddleware

        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.CORS_ALLOWED_ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
            expose_headers=settings.CORS_EXPOSE_HEADERS,
        )


def register_router(app: FastAPI):
    dependencies = [Depends(demo_site)] if settings.DEMO_MODE else None
    app.include_router(route, dependencies=dependencies)
    ensure_unique_route_names(app)
    simplify_operation_ids(app)


def register_page(app: FastAPI):
    add_pagination(app)
