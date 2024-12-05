from sqlalchemy import Select, desc, func, select
from sqlalchemy_crud_plus import CRUDPlus
from sqlalchemy.ext.asyncio import AsyncSession

from app.user.model.sys_smart import Smart
from app.user.schema.product import (
    CreateProductParam,
    GetProductInfoListDetails,
    GetProductInfoDetails,
)


class CRUDSmart(CRUDPlus[Smart]):

    async def get_list(self) -> GetProductInfoListDetails | None:
        """
        Получить список созданных smart процессов


        :return:
        """
        stmt = select(self.model).order_by(desc(self.model.name))
        return stmt

    async def create(self, db: AsyncSession, obj_in: CreateProductParam):
        await self.create_model(db, obj=obj_in, commit=True)


smart_dao: CRUDSmart = CRUDSmart(Smart)
