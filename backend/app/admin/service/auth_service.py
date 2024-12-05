from fastapi import Request, Response
from fastapi.security import HTTPBasicCredentials
from starlette.background import BackgroundTask, BackgroundTasks

from app.admin.conf import admin_settings
from app.admin.crud.crud_user import user_dao
from app.admin.model.sys_user import User
from app.admin.schema.token import GetLoginToken, GetNewToken
from app.admin.schema.user import AuthLoginParam
from app.admin.service.login_log_service import LoginLogService
from common.enums import LoginLogStatusType
from common.exception import errors
from common.response.response_code import CustomErrorCode
from common.security.jwt import (
    create_access_token,
    create_new_token,
    create_refresh_token,
    get_token,
    jwt_decode,
    password_verify,
)
from core.config import settings
from database.db_postgres import async_session
from database.db_redis import redis_client
from utils.timezone import timezone


class AuthService:
    @staticmethod
    async def swagger_login(*, obj: HTTPBasicCredentials) -> tuple[str, User]:
        async with async_session.begin() as db:
            current_user = await user_dao.get_by_username(db, obj.username)
            if not current_user:
                raise errors.NotFoundError(msg="Неверное имя пользователя или пароль")
            elif not password_verify(
                f"{obj.password}{current_user.salt}", current_user.password
            ):
                raise errors.AuthorizationError(
                    msg="Неверное имя пользователя или пароль"
                )
            elif not current_user.status:
                raise errors.AuthorizationError(
                    msg="Пользователь был заблокирован, пожалуйста, обратитесь к системному администратору"
                )
            access_token = await create_access_token(
                str(current_user.id), current_user.is_multi_login
            )
            await user_dao.update_login_time(db, obj.username)
            return access_token.access_token, current_user

    @staticmethod
    async def login(
        *,
        request: Request,
        response: Response,
        obj: AuthLoginParam,
        background_tasks: BackgroundTasks,
    ) -> GetLoginToken:
        async with async_session.begin() as db:
            try:
                current_user = await user_dao.get_with_relation(
                    db, username=obj.username
                )
                if not current_user:
                    raise errors.NotFoundError(
                        msg="Неверное имя пользователя или пароль"
                    )
                user_uuid = current_user.uuid
                username = current_user.username
                if not password_verify(
                    obj.password + current_user.salt, current_user.password
                ):
                    raise errors.NotFoundError(
                        msg="Неверное имя пользователя или пароль"
                    )
                elif not current_user.status:
                    raise errors.NotFoundError(
                        msg="Пользователь был заблокирован, пожалуйста, обратитесь к системному администратору"
                    )
                current_user_id = current_user.id
                access_token = await create_access_token(
                    str(current_user_id), current_user.is_multi_login
                )
                refresh_token = await create_refresh_token(
                    str(current_user_id), current_user.is_multi_login
                )
            except errors.NotFoundError as e:
                raise errors.NotFoundError(msg=e.msg)
            except (errors.AuthorizationError, errors.CustomError) as e:
                task = BackgroundTask(
                    LoginLogService.create,
                    **dict(
                        db=db,
                        request=request,
                        user_uuid=user_uuid,
                        username=username,
                        login_time=timezone.now(),
                        status=LoginLogStatusType.fail.value,
                        msg=e.msg,
                    ),
                )
                raise errors.AuthorizationError(msg=e.msg, background=task)
            except Exception as e:
                raise e
            else:
                background_tasks.add_task(
                    LoginLogService.create,
                    **dict(
                        db=db,
                        request=request,
                        user_uuid=user_uuid,
                        username=username,
                        login_time=timezone.now(),
                        status=LoginLogStatusType.success.value,
                        msg="Успешный вход в систему",
                    ),
                )
                await redis_client.delete(
                    f"{admin_settings.CAPTCHA_LOGIN_REDIS_PREFIX}:{request.state.ip}"
                )
                await user_dao.update_login_time(db, obj.username)
                response.set_cookie(
                    key=settings.COOKIE_REFRESH_TOKEN_KEY,
                    value=refresh_token.refresh_token,
                    max_age=settings.COOKIE_REFRESH_TOKEN_EXPIRE_SECONDS,
                    expires=timezone.f_utc(refresh_token.refresh_token_expire_time),
                    httponly=True,
                )
                await db.refresh(current_user)
                data = GetLoginToken(
                    access_token=access_token.access_token,
                    access_token_expire_time=access_token.access_token_expire_time,
                    user=current_user,  # type: ignore
                )
                return data

    @staticmethod
    async def login_capcha(
        *,
        request: Request,
        response: Response,
        obj: AuthLoginParam,
        background_tasks: BackgroundTasks,
    ) -> GetLoginToken:
        async with async_session.begin() as db:
            try:
                current_user = await user_dao.get_by_username(db, obj.username)
                if not current_user:
                    raise errors.NotFoundError(
                        msg="Неверное имя пользователя или пароль"
                    )
                user_uuid = current_user.uuid
                username = current_user.username
                if not password_verify(
                    obj.password + current_user.salt, current_user.password
                ):
                    raise errors.NotFoundError(
                        msg="Неверное имя пользователя или пароль"
                    )
                elif not current_user.status:
                    raise errors.NotFoundError(
                        msg="Пользователь был заблокирован, пожалуйста, обратитесь к системному администратору"
                    )
                captcha_code = await redis_client.get(
                    f"{admin_settings.CAPTCHA_LOGIN_REDIS_PREFIX}:{request.state.ip}"
                )
                if not captcha_code:
                    raise errors.NotFoundError(
                        msg="Проверочный код неверен, пожалуйста, введите его еще раз"
                    )
                if captcha_code.lower() != obj.captcha.lower():
                    raise errors.CustomError(error=CustomErrorCode.CAPTCHA_ERROR)
                current_user_id = current_user.id
                access_token = await create_access_token(
                    str(current_user_id), current_user.is_multi_login
                )
                refresh_token = await create_refresh_token(
                    str(current_user_id), current_user.is_multi_login
                )
            except errors.NotFoundError as e:
                raise errors.NotFoundError(msg=e.msg)
            except (errors.AuthorizationError, errors.CustomError) as e:
                task = BackgroundTask(
                    LoginLogService.create,
                    **dict(
                        db=db,
                        request=request,
                        user_uuid=user_uuid,
                        username=username,
                        login_time=timezone.now(),
                        status=LoginLogStatusType.fail.value,
                        msg=e.msg,
                    ),
                )
                raise errors.AuthorizationError(msg=e.msg, background=task)
            except Exception as e:
                raise e
            else:
                background_tasks.add_task(
                    LoginLogService.create,
                    **dict(
                        db=db,
                        request=request,
                        user_uuid=user_uuid,
                        username=username,
                        login_time=timezone.now(),
                        status=LoginLogStatusType.success.value,
                        msg="登录成功",
                    ),
                )
                await redis_client.delete(
                    f"{admin_settings.CAPTCHA_LOGIN_REDIS_PREFIX}:{request.state.ip}"
                )
                await user_dao.update_login_time(db, obj.username)
                response.set_cookie(
                    key=settings.COOKIE_REFRESH_TOKEN_KEY,
                    value=refresh_token.refresh_token,
                    max_age=settings.COOKIE_REFRESH_TOKEN_EXPIRE_SECONDS,
                    expires=timezone.f_utc(refresh_token.refresh_token_expire_time),
                    httponly=True,
                )
                await db.refresh(current_user)
                data = GetLoginToken(
                    access_token=access_token.access_token,
                    access_token_expire_time=access_token.access_token_expire_time,
                    user=current_user,  # type: ignore
                )
                return data

    @staticmethod
    async def new_token(*, request: Request, response: Response) -> GetNewToken:
        refresh_token = request.cookies.get(settings.COOKIE_REFRESH_TOKEN_KEY)
        if not refresh_token:
            raise errors.TokenError(
                msg="Refresh Token потерян, пожалуйста, войдите в систему еще раз"
            )
        try:
            user_id = jwt_decode(refresh_token)
        except Exception:
            raise errors.TokenError(msg="Refresh Token недействительный")
        if request.user.id != user_id:
            raise errors.TokenError(msg="Refresh Token недействительный")
        async with async_session() as db:
            current_user = await user_dao.get(db, user_id)
            if not current_user:
                raise errors.NotFoundError(msg="Неверное имя пользователя или пароль")
            elif not current_user.status:
                raise errors.NotFoundError(
                    msg="Пользователь был заблокирован, пожалуйста, обратитесь к системному администратору"
                )
            current_token = get_token(request)
            new_token = await create_new_token(
                sub=str(current_user.id),
                token=current_token,
                refresh_token=refresh_token,
                multi_login=current_user.is_multi_login,
            )
            response.set_cookie(
                key=settings.COOKIE_REFRESH_TOKEN_KEY,
                value=new_token.new_refresh_token,
                max_age=settings.COOKIE_REFRESH_TOKEN_EXPIRE_SECONDS,
                expires=timezone.f_utc(new_token.new_refresh_token_expire_time),
                httponly=True,
            )
            data = GetNewToken(
                access_token=new_token.new_access_token,
                access_token_expire_time=new_token.new_access_token_expire_time,
            )
            return data

    @staticmethod
    async def logout(*, request: Request, response: Response) -> None:
        token = get_token(request)
        refresh_token = request.cookies.get(settings.COOKIE_REFRESH_TOKEN_KEY)
        response.delete_cookie(settings.COOKIE_REFRESH_TOKEN_KEY)
        if request.user.is_multi_login:
            key = f"{settings.TOKEN_REDIS_PREFIX}:{request.user.id}:{token}"
            await redis_client.delete(key)
            if refresh_token:
                key = f"{settings.TOKEN_REFRESH_REDIS_PREFIX}:{request.user.id}:{refresh_token}"
                await redis_client.delete(key)
        else:
            key_prefix = f"{settings.TOKEN_REDIS_PREFIX}:{request.user.id}:"
            await redis_client.delete_prefix(key_prefix)
            key_prefix = f"{settings.TOKEN_REFRESH_REDIS_PREFIX}:{request.user.id}:"
            await redis_client.delete_prefix(key_prefix)


auth_service = AuthService()
