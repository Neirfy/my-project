from typing import Sequence

from fastapi import Request
from sqlalchemy import Select

from app.admin.crud.crud_menu import menu_dao
from app.admin.crud.crud_role import role_dao
from app.admin.model.sys_role import Role
from app.admin.schema.role import CreateRoleParam, UpdateRoleMenuParam, UpdateRoleParam
from common.exception import errors
from core.config import settings
from database.db_postgres import async_session
from database.db_redis import redis_client


class RoleService:
    @staticmethod
    async def get(*, pk: int) -> Role:
        async with async_session() as db:
            role = await role_dao.get_with_relation(db, pk)
            if not role:
                raise errors.NotFoundError(msg='Этой роли не существует')
            return role

    @staticmethod
    async def get_all() -> Sequence[Role]:
        async with async_session() as db:
            roles = await role_dao.get_all(db)
            return roles

    @staticmethod
    async def get_user_roles(*, pk: int) -> Sequence[Role]:
        async with async_session() as db:
            roles = await role_dao.get_user_roles(db, user_id=pk)
            return roles

    @staticmethod
    async def get_select(*, name: str = None, data_scope: int = None, status: int = None) -> Select:
        return await role_dao.get_list(name=name, data_scope=data_scope, status=status)

    @staticmethod
    async def create(*, obj: CreateRoleParam) -> None:
        async with async_session.begin() as db:
            role = await role_dao.get_by_name(db, obj.name)
            if role:
                raise errors.ForbiddenError(msg='Эта роль уже существует')
            await role_dao.create(db, obj)

    @staticmethod
    async def update(*, pk: int, obj: UpdateRoleParam) -> int:
        async with async_session.begin() as db:
            role = await role_dao.get(db, pk)
            if not role:
                raise errors.NotFoundError(msg='Этой роли не существует')
            if role.name != obj.name:
                role = await role_dao.get_by_name(db, obj.name)
                if role:
                    raise errors.ForbiddenError(msg='Эта роль уже существует')
            count = await role_dao.update(db, pk, obj)
            return count

    @staticmethod
    async def update_role_menu(*, request: Request, pk: int, menu_ids: UpdateRoleMenuParam) -> int:
        async with async_session.begin() as db:
            role = await role_dao.get(db, pk)
            if not role:
                raise errors.NotFoundError(msg='Этой роли не существует')
            for menu_id in menu_ids.menus:
                menu = await menu_dao.get(db, menu_id)
                if not menu:
                    raise errors.NotFoundError(msg='Меню не существует')
            count = await role_dao.update_menus(db, pk, menu_ids)
            if pk in [role.id for role in request.user.roles]:
                await redis_client.delete_prefix(f'{settings.PERMISSION_REDIS_PREFIX}:{request.user.uuid}')
                await redis_client.delete(f'{settings.JWT_USER_REDIS_PREFIX}:{request.user.id}')
            return count

    @staticmethod
    async def delete(*, pk: list[int]) -> int:
        async with async_session.begin() as db:
            count = await role_dao.delete(db, pk)
            return count


role_service = RoleService()