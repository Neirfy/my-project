from sqlalchemy import Select, desc, func, select
from sqlalchemy_crud_plus import CRUDPlus
from sqlalchemy.ext.asyncio import AsyncSession

from app.user.model.sys_product import Product
from app.user.schema.product import (
    CreateProductParam,
    GetProductInfoListDetails,
    GetProductInfoDetails,
    UpdateProductQuantityParam,
)
from common.exception import errors
from database.db_postgres import async_session


class CRUDProduct(CRUDPlus[Product]):
    async def get_list(self) -> GetProductInfoListDetails | None:
        """
        Получить список Продуктов


        :return:
        """
        stmt = select(self.model).order_by(desc(self.model.name))
        return stmt

    async def get_list_with_quantity(self) -> GetProductInfoListDetails | None:
        """
        Получить список Продуктов


        :return:
        """
        stmt = (
            select(self.model)
            .order_by(desc(self.model.name))
            .where(self.model.quantity > 0)
        )
        return stmt

    async def get_product(
        self, db: AsyncSession, product_id: int
    ) -> GetProductInfoDetails | None:
        """
        Получить Продукт по id

        :param db:
        :param product_id:

        :return:
        """
        stmt = select(self.model).where(self.model.id == product_id)
        product = await db.execute(stmt.where(self.model.id == product_id))
        return product.scalars().first()

    async def search_product(self, query) -> Select:
        """
        Получить список товаров по фильтру


        :return:
        """
        stmt = select(self.model).filter(
            func.lower(self.model.name).contains(func.lower(query))
        )
        return stmt

    async def search_product_with_quantity(self, query) -> Select:
        stmt = (
            select(self.model)
            .filter(func.lower(self.model.name).contains(func.lower(query)))
            .where(self.model.quantity > 0)
        )
        return stmt

    async def create(self, db: AsyncSession, obj_in: CreateProductParam):
        await self.create_model(db, obj=obj_in, commit=True)

    async def update(self, db: AsyncSession, obj_in: CreateProductParam):
        stmt = select(self.model).where(self.model.uuid == obj_in.uuid)
        product = await db.execute(stmt)
        pk = product.scalars().first()
        await self.update_model(db, pk=pk.id, obj=obj_in, commit=True)

    async def update_quantity(self, db: AsyncSession, pk: int, quantity: int):
        stmt = select(self.model).where(self.model.id == pk)
        product = await db.execute(stmt)
        product = product.scalars().first()
        if product:
            if product.quantity - quantity < 0:
                raise errors.ForbiddenError(msg="Количество не может быть меньше 0")
            product.quantity -= quantity
            updated_product = UpdateProductQuantityParam(
                **{"id": product.id, "quantity": product.quantity}
            )
            await self.update_model(db, pk=pk, obj=updated_product, commit=True)

    async def verify_quantity(self, db: AsyncSession, pk: int, quantity: int):
        stmt = select(self.model).where(self.model.id == pk)
        product = await db.execute(stmt)
        product = product.scalars().first()
        if product:
            if product.quantity - quantity < 0:
                raise errors.ForbiddenError(msg="Количество не может быть меньше 0")

product_dao: CRUDProduct = CRUDProduct(Product)
