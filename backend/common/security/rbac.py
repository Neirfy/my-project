import casbin
import casbin_async_sqlalchemy_adapter

from fastapi import Depends, Request

from app.admin.model.sys_casbin_rule import CasbinRule
from common.enums import MethodType, StatusType
from common.exception.errors import AuthorizationError, TokenError
from common.security.jwt import DependsJwtAuth
from core.config import settings
from database.db_postgres import async_engine


class RBAC:
    @staticmethod
    async def enforcer() -> casbin.AsyncEnforcer:
        _CASBIN_RBAC_MODEL_CONF_TEXT = """
        [request_definition]
        r = sub, obj, act

        [policy_definition]
        p = sub, obj, act

        [role_definition]
        g = _, _

        [policy_effect]
        e = some(where (p.eft == allow))

        [matchers]
        m = g(r.sub, p.sub) && (keyMatch(r.obj, p.obj) || keyMatch3(r.obj, p.obj)) && (r.act == p.act || p.act == "*")
        """
        adapter = casbin_async_sqlalchemy_adapter.Adapter(
            async_engine, db_class=CasbinRule
        )
        model = casbin.AsyncEnforcer.new_model(text=_CASBIN_RBAC_MODEL_CONF_TEXT)
        enforcer = casbin.AsyncEnforcer(model, adapter)
        await enforcer.load_policy()
        return enforcer

    async def rbac_verify(self, request: Request, _token: str = DependsJwtAuth) -> None:
        """
        RBAC Проверка разрешений

        :param request:
        :param _token:
        :return:
        """
        path = request.url.path
        # Белый список для проверки подлинности
        if path in settings.TOKEN_REQUEST_PATH_EXCLUDE:
            return
        # JWT Обязательная проверка статуса авторизации
        if not request.auth.scopes:
            raise TokenError
        # Верификация суперадминистратора-бесплатно
        if request.user.is_superuser:
            return
        # Определение объема полномочий по обработке данных роли
        user_roles = request.user.roles
        if not user_roles:
            raise AuthorizationError(
                msg="Пользователю не назначена роль, и авторизация не удалась"
            )
        if not any(len(role.menus) > 0 for role in user_roles):
            raise AuthorizationError(
                msg="Роли, к которой принадлежит пользователь, не назначено меню, и авторизация не удалась"
            )
        method = request.method
        if method != MethodType.GET or method != MethodType.OPTIONS:
            if not request.user.is_staff:
                raise AuthorizationError(
                    msg="Этому пользователю было запрещено выполнять операции фонового управления"
                )
        # Объем полномочий по обработке данных
        data_scope = any(role.data_scope == 1 for role in user_roles)
        if data_scope:
            return
        user_uuid = request.user.uuid
        if settings.PERMISSION_MODE == "role-menu":
            # Проверка прав доступа к меню ролей
            path_auth_perm = getattr(request.state, "permission", None)
            # Нет, идентификатор разрешения доступа к меню не подтвержден
            if not path_auth_perm:
                return
            if path_auth_perm in set(settings.RBAC_ROLE_MENU_EXCLUDE):
                return
            allow_perms = []
            for role in user_roles:
                for menu in role.menus:
                    if menu.status == StatusType.enable:
                        allow_perms.extend(menu.perms.split(","))
            if path_auth_perm not in allow_perms:
                raise AuthorizationError
        else:
            # casbin Проверка разрешений
            if (method, path) in settings.RBAC_CASBIN_EXCLUDE:
                return
            enforcer = await self.enforcer()
            if not enforcer.enforce(user_uuid, path, method):
                raise AuthorizationError


rbac = RBAC()

DependsRBAC = Depends(rbac.rbac_verify)
