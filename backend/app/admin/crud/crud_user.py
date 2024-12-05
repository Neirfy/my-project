from fast_captcha import text_captcha
from sqlalchemy import and_, desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import Select
from sqlalchemy_crud_plus import CRUDPlus

from app.admin.model.sys_role import Role
from app.admin.model.sys_user import User

from app.admin.schema.user import (
    AddUserParam,
    AvatarParam,
    RegisterUserParam,
    UpdateUserParam,
    UpdateUserRoleParam,
)
from common.security.jwt import get_hash_password
from utils.timezone import timezone


class CRUDUser(CRUDPlus[User]):
    async def get(self, db: AsyncSession, user_id: int) -> User | None:
        return await self.select_model(db, user_id)

    async def get_by_username(self, db: AsyncSession, username: str) -> User | None:
        return await self.select_model_by_column(db, username=username)

    async def get_by_nickname(self, db: AsyncSession, nickname: str) -> User | None:
        return await self.select_model_by_column(db, nickname=nickname)

    async def update_login_time(self, db: AsyncSession, username: str) -> int:
        return await self.update_model_by_column(
            db, {"last_login_time": timezone.now()}, username=username
        )

    async def create(
        self, db: AsyncSession, obj: RegisterUserParam, *, social: bool = False
    ) -> None:
        if not social:
            salt = text_captcha(5)
            obj.password = get_hash_password(f"{obj.password}{salt}")
            dict_obj = obj.model_dump()
            dict_obj.update({"is_staff": True, "salt": salt})
        else:
            dict_obj = obj.model_dump()
            dict_obj.update({"is_staff": True, "salt": None})
        new_user = self.model(**dict_obj)
        db.add(new_user)

    async def add(self, db: AsyncSession, obj: AddUserParam) -> None:
        salt = text_captcha(5)
        obj.password = get_hash_password(f"{obj.password}{salt}")
        dict_obj = obj.model_dump(exclude={"roles"})
        dict_obj.update({"salt": salt})
        new_user = self.model(**dict_obj)
        role_list = []
        for role_id in obj.roles:
            role_list.append(await db.get(Role, role_id))
        new_user.roles.extend(role_list)
        db.add(new_user)

    async def update_userinfo(
        self, db: AsyncSession, input_user: int, obj: UpdateUserParam
    ) -> int:
        return await self.update_model(db, input_user, obj)

    @staticmethod
    async def update_role(
        db: AsyncSession, input_user: User, obj: UpdateUserRoleParam
    ) -> None:
        for i in list(input_user.roles):
            input_user.roles.remove(i)
        role_list = []
        for role_id in obj.roles:
            role_list.append(await db.get(Role, role_id))
        input_user.roles.extend(role_list)

    async def update_avatar(
        self, db: AsyncSession, input_user: int, avatar: AvatarParam
    ) -> int:

        return await self.update_model(db, input_user, {"avatar": avatar.url})

    async def delete(self, db: AsyncSession, user_id: int) -> int:
        return await self.delete_model(db, user_id)

    async def check_email(self, db: AsyncSession, email: str) -> User | None:
        return await self.select_model_by_column(db, email=email)

    async def reset_password(self, db: AsyncSession, pk: int, new_pwd: str) -> int:
        return await self.update_model(db, pk, {"password": new_pwd})

    async def get_list(
        self,
        dept: int = None,
        username: str = None,
        phone: str = None,
        status: int = None,
    ) -> Select:
        stmt = (
            select(self.model)
            .options(selectinload(self.model.dept))
            .options(selectinload(self.model.roles).selectinload(Role.menus))
            .order_by(desc(self.model.join_time))
        )
        where_list = []
        if dept:
            where_list.append(self.model.dept_id == dept)
        if username:
            where_list.append(self.model.username.like(f"%{username}%"))
        if phone:
            where_list.append(self.model.phone.like(f"%{phone}%"))
        if status is not None:
            where_list.append(self.model.status == status)
        if where_list:
            stmt = stmt.where(and_(*where_list))
        return stmt

    async def get_super(self, db: AsyncSession, user_id: int) -> bool:
        user = await self.get(db, user_id)
        return user.is_superuser

    async def get_staff(self, db: AsyncSession, user_id: int) -> bool:
        user = await self.get(db, user_id)
        return user.is_staff

    async def get_status(self, db: AsyncSession, user_id: int) -> int:
        user = await self.get(db, user_id)
        return user.status

    async def get_multi_login(self, db: AsyncSession, user_id: int) -> bool:
        user = await self.get(db, user_id)
        return user.is_multi_login

    async def set_super(self, db: AsyncSession, user_id: int, _super: bool) -> int:
        return await self.update_model(db, user_id, {"is_superuser": _super})

    async def set_staff(self, db: AsyncSession, user_id: int, staff: bool) -> int:
        return await self.update_model(db, user_id, {"is_staff": staff})

    async def set_status(self, db: AsyncSession, user_id: int, status: bool) -> int:
        return await self.update_model(db, user_id, {"status": status})

    async def set_multi_login(
        self, db: AsyncSession, user_id: int, multi_login: bool
    ) -> int:
        return await self.update_model(db, user_id, {"is_multi_login": multi_login})

    async def get_with_relation(
        self, db: AsyncSession, *, user_id: int = None, username: str = None
    ) -> User | None:
        stmt = (
            select(self.model)
            .options(selectinload(self.model.dept))
            .options(selectinload(self.model.roles).joinedload(Role.menus))
        )
        filters = []
        if user_id:
            filters.append(self.model.id == user_id)
        if username:
            filters.append(self.model.username == username)
        user = await db.execute(stmt.where(*filters))
        return user.scalars().first()


user_dao: CRUDUser = CRUDUser(User)
