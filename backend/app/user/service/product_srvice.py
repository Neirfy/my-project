from sqlalchemy import Select

from database.db_postgres import async_session
from app.user.crud.crud_product import product_dao
from app.user.schema.product import GetProductInfoDetails
from common.exception import errors


class ProductService:
    @staticmethod
    async def get() -> Select:
        return await product_dao.get_list()

    @staticmethod
    async def get_select(*, product_id: int) -> GetProductInfoDetails:
        async with async_session() as db:
            product = await product_dao.get_product(db, product_id=product_id)
            if not product:
                raise errors.NotFoundError(msg="Продукт не существует")
            return product

    @staticmethod
    async def get_select_with_quantity() -> Select:
        return await product_dao.get_list_with_quantity()

    @staticmethod
    async def search_product(*, query: str) -> Select:
        return await product_dao.search_product(query=query)

    @staticmethod
    async def search_product_with_quantity(*, query: str) -> Select:
        return await product_dao.search_product_with_quantity(query=query)

    @staticmethod
    async def update_quantity(*, product_id: int, quantity: int):
        async with async_session() as db:
            product = await product_dao.update_quantity(
                db, product_id=product_id, quantity=quantity
            )
            if not product:
                raise errors.NotFoundError(msg="Продукт не существует")
            return product


product_service = ProductService()
