from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy_crud_plus import CRUDPlus

from app.admin.model.sys_user import User
from app.admin.model.sys_dept import Dept

from app.admin.schema.dept import CreateDeptParam, UpdateDeptParam


class CRUDDept(CRUDPlus[Dept]):
    async def get(self, db: AsyncSession, dept_id: int) -> Dept | None:
        return await self.select_model_by_column(db, id=dept_id, del_flag=False)

    async def get_by_name(self, db: AsyncSession, name: str) -> Dept | None:
        return await self.select_model_by_column(db, name=name, del_flag=False)

    async def get_all(
        self,
        db: AsyncSession,
        name: str = None,
        leader: str = None,
        phone: str = None,
        status: int = None,
    ) -> Sequence[Dept]:
        filters = {"del_flag__eq": False}
        if name is not None:
            filters.update(name__like=f"%{name}%")
        if leader is not None:
            filters.update(leader__like=f"%{leader}%")
        if phone is not None:
            filters.update(phone__startswith=phone)
        if status is not None:
            filters.update(status=status)
        return await self.select_models_order(db, sort_columns="sort", **filters)

    async def create(self, db: AsyncSession, obj_in: CreateDeptParam) -> None:
        await self.create_model(db, obj_in)

    async def update(
        self, db: AsyncSession, dept_id: int, obj_in: UpdateDeptParam
    ) -> int:
        return await self.update_model(db, dept_id, obj_in)

    async def delete(self, db: AsyncSession, dept_id: int) -> int:
        return await self.delete_model_by_column(
            db, id=dept_id, logical_deletion=True, deleted_flag_column="del_flag"
        )

    async def get_with_relation(self, db: AsyncSession, dept_id: int) -> list[User]:
        stmt = (
            select(self.model)
            .options(selectinload(self.model.users))
            .where(self.model.id == dept_id)
        )
        result = await db.execute(stmt)
        user_relation = result.scalars().first()
        return user_relation.users

    async def get_children(self, db: AsyncSession, dept_id: int) -> list[Dept]:
        stmt = (
            select(self.model)
            .options(selectinload(self.model.children))
            .where(self.model.id == dept_id)
        )
        result = await db.execute(stmt)
        dept = result.scalars().first()
        return dept.children


dept_dao: CRUDDept = CRUDDept(Dept)
