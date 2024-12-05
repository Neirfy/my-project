from sqlalchemy import Select, desc, func, select
from sqlalchemy_crud_plus import CRUDPlus
from sqlalchemy.ext.asyncio import AsyncSession

from app.user.schema.object import CreateObjectParam, GetObjectInfoDetails
from app.user.model.sys_object import Object


class CRUDObject(CRUDPlus[Object]):
    async def create(self, db: AsyncSession, obj_in: CreateObjectParam):
        await self.create_model(db, obj_in, commit=True)

    async def update(self, db: AsyncSession, obj_in: CreateObjectParam):
        await self.update_model(db, pk=obj_in.id, obj=obj_in, commit=True)

    async def get_list(self) -> Select:
        """
        Получить список Объектов


        :return:
        """
        stmt = select(self.model).order_by(desc(self.model.name))
        return stmt

    async def get_object(
        self, db: AsyncSession, object_id: int
    ) -> GetObjectInfoDetails | None:
        """
        Получить Объект по id

        :param db:
        :param product_id:

        :return:
        """
        stmt = select(self.model).where(self.model.id == object_id)
        object = await db.execute(stmt.where(self.model.id == object_id))
        return object.scalars().first()

    # search_object
    async def search_object(self, query) -> Select:
        """
        Получить список Объектов


        :return:
        """
        stmt = select(self.model).filter(
            func.lower(self.model.name).contains(func.lower(query))
        )
        return stmt


object_dao: CRUDObject = CRUDObject(Object)
