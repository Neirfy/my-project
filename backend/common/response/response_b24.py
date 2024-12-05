import requests

from core.config import settings

from sqlalchemy.exc import IntegrityError
from app.user.schema.object import CreateObjectParam
from app.user.crud.crud_object import object_dao
from database.db_postgres import async_session
from app.user.schema.smart import CreateSmart


class Bitrix24:

    def __init__(self):
        self.b24_url = settings.BITRIX_HOOK
        self.b24_user_url = settings.BITRIX_HOOK_USER

    async def get_objects(self):
        data = {
            "IBLOCK_TYPE_ID": "lists",
            "IBLOCK_ID": "29",
        }

        request = requests.post(f"{self.b24_url}/lists.element.get", json=data)
        objects = request.json()

        for object in objects.get("result", {}):
            object_format = {
                "id": int(object.get("ID")),
                "name": object.get("NAME", None),
                "address": list(object.get("PROPERTY_107", {}).values())[0],
            }
            object_data = CreateObjectParam(**object_format)
            try:
                async with async_session() as session:
                    await object_dao.create(session, object_data)

            except IntegrityError:
                async with async_session() as session:
                    await object_dao.update(session, object_data)

    def create_smart_process(self, smart_process: CreateSmart):
        products = []
        for product in smart_process.products:
            products.append(f"{product.name} - {product.quantity} шт.")

        products_str = "\n".join(products)

        data = {
            "entityTypeId": settings.ENTITY_TYPE_ID,
            "fields": {
                "title": "",
                f"{settings.FIELD_PRODUCT}": products_str,  # Позиции для закупки
                f"{settings.FIELD_NAME}": f"{smart_process.name}",  # ФИО монтажника
                f"{settings.FIELD_OBJECT}": f"{smart_process.object}",  # Объект
                f"{settings.FIELD_ADDRESS}": f"{smart_process.address}",  # Адрес доставки
                f"{settings.FIELD_DATE}": f"{smart_process.date}",  # Сроки поставки
                f"{settings.FIELD_URGENCY}": str(
                    smart_process.urgency
                ).lower(),  # Срочность
                f"{settings.FIELD_COMMENT}": f"{smart_process.comment}",  # Комментарий
                # f"assigned_by_id": "",  # Ответственный
            },
        }
        print(data)

        request = requests.post(f"{self.b24_url}/crm.item.add", json=data)
        return request.json()

    async def get_users(self):
        request = requests.post(f"{self.b24_user_url}/lists.element.get")
        return request
