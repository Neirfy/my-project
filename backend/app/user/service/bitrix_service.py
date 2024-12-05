from sqlalchemy import Select

from app.user.schema.smart import CreateSmart
from common.response.response_b24 import Bitrix24
from app.user.crud.crud_product import product_dao

from common.exception import errors
from common.response.response_code import CustomErrorCode, CustomResponseCode
from database.db_postgres import async_session


class BitrixService:

    @staticmethod
    async def create_smart(response_model: CreateSmart) -> Select:
        try:
            for product in response_model.products:
                async with async_session() as db:
                    await product_dao.verify_quantity(
                        db, pk=product.id, quantity=product.quantity
                    )
        except:
            raise errors.CustomError(error=CustomResponseCode.HTTP_425)
        try:

            responce = Bitrix24().create_smart_process(response_model)
            for product in response_model.products:
                async with async_session() as db:
                    await product_dao.update_quantity(
                        db, pk=product.id, quantity=product.quantity
                    )
            return responce
        except:
            raise errors.CustomError(error=CustomErrorCode.BITRIX_ERROR)


bitrix_service = BitrixService()
