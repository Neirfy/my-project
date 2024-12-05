from sqlalchemy import Select

from database.db_postgres import async_session
from app.user.crud.crud_object import object_dao
from common.exception import errors


class ObjectService:
    @staticmethod
    async def get() -> Select:
        return await object_dao.get_list()

    @staticmethod
    async def get_select(*, object_id: int) -> Select:
        async with async_session() as db:
            object = await object_dao.get_object(db, object_id=object_id)
            if not object:
                raise errors.NotFoundError(msg="Объект не существует")
            return object

    @staticmethod
    async def search_object(*, query: str):
        return await object_dao.search_object(query=query)


object_service = ObjectService()
