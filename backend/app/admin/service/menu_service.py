from typing import Any

from fastapi import Request

from app.admin.crud.crud_menu import menu_dao
from app.admin.crud.crud_role import role_dao
from app.admin.model.sys_menu import Menu
from app.admin.schema.menu import CreateMenuParam, UpdateMenuParam
from common.exception import errors
from core.config import settings
from database.db_postgres import async_session
from database.db_redis import redis_client
from utils.build_tree import get_tree_data


class MenuService:
    @staticmethod
    async def get(*, pk: int) -> Menu:
        async with async_session() as db:
            menu = await menu_dao.get(db, menu_id=pk)
            if not menu:
                raise errors.NotFoundError(msg="Меню не существует")
            return menu

    @staticmethod
    async def get_menu_tree(
        *, title: str | None = None, status: int | None = None
    ) -> list[dict[str, Any]]:
        async with async_session() as db:
            menu_select = await menu_dao.get_all(db, title=title, status=status)
            menu_tree = get_tree_data(menu_select)
            return menu_tree

    @staticmethod
    async def get_role_menu_tree(*, pk: int) -> list[dict[str, Any]]:
        async with async_session() as db:
            role = await role_dao.get_with_relation(db, pk)
            if not role:
                raise errors.NotFoundError(msg="Эта роль не существует")
            menu_ids = [menu.id for menu in role.menus]
            menu_select = await menu_dao.get_role_menus(db, False, menu_ids)
            menu_tree = get_tree_data(menu_select)
            return menu_tree

    @staticmethod
    async def get_user_menu_tree(*, request: Request) -> list[dict[str, Any]]:
        async with async_session() as db:
            roles = request.user.roles
            menu_ids = []
            menu_tree = []
            if roles:
                for role in roles:
                    menu_ids.extend([menu.id for menu in role.menus])
                menu_select = await menu_dao.get_role_menus(
                    db, request.user.is_superuser, menu_ids
                )
                menu_tree = get_tree_data(menu_select)
            return menu_tree

    @staticmethod
    async def create(*, obj: CreateMenuParam) -> None:
        async with async_session.begin() as db:
            title = await menu_dao.get_by_title(db, obj.title)
            if title:
                raise errors.ForbiddenError(msg="Название меню уже существует")
            if obj.parent_id:
                parent_menu = await menu_dao.get(db, obj.parent_id)
                if not parent_menu:
                    raise errors.NotFoundError(msg="Родительское меню не существует")
            await menu_dao.create(db, obj)

    @staticmethod
    async def update(*, pk: int, obj: UpdateMenuParam) -> int:
        async with async_session.begin() as db:
            menu = await menu_dao.get(db, pk)
            if not menu:
                raise errors.NotFoundError(msg="Меню не существует")
            if menu.title != obj.title:
                if await menu_dao.get_by_title(db, obj.title):
                    raise errors.ForbiddenError(msg="Название меню уже существует")
            if obj.parent_id:
                parent_menu = await menu_dao.get(db, obj.parent_id)
                if not parent_menu:
                    raise errors.NotFoundError(msg="Родительское меню не существует")
            if obj.parent_id == menu.id:
                raise errors.ForbiddenError(
                    msg="Запретить ассоциировать себя с родителями"
                )
            count = await menu_dao.update(db, pk, obj)
            await redis_client.delete_prefix(settings.PERMISSION_REDIS_PREFIX)
            return count

    @staticmethod
    async def delete(*, pk: int) -> int:
        async with async_session.begin() as db:
            children = await menu_dao.get_children(db, pk)
            if children:
                raise errors.ForbiddenError(
                    msg="В меню есть подменю, которое нельзя удалить"
                )
            count = await menu_dao.delete(db, pk)
            return count


menu_service = MenuService()
