from bs4 import BeautifulSoup
from core.path_conf import STORE_DIR
from sqlalchemy.exc import IntegrityError
from app.user.schema.product import CreateProductParam
from app.user.crud.crud_product import product_dao
from database.db_postgres import async_session


class OneCParser:
    def __init__(self):
        self.path = STORE_DIR

    def read_from_file(self, filename):
        with open(f"{self.path}/{filename}", "r", encoding="utf-8") as fp:
            xml_string = fp.read()

        soup = BeautifulSoup(xml_string, features="xml")
        return soup

    async def create_products(self, filename):
        soup = self.read_from_file(filename)
        products = soup.find("Предложения")

        if products is not None:
            for product in products.find_all("Предложение"):
                product_format = {
                    "uuid": product.find("Ид").text,
                    "image": None,
                    "name": product.find("Наименование").text,
                    "quantity": int(product.find("Склад").get("КоличествоНаСкладе")),
                }

                product_data = CreateProductParam(**product_format)

                try:
                    async with async_session() as session:
                        await product_dao.create(session, product_data)

                except IntegrityError:
                    async with async_session() as session:
                        await product_dao.update(session, product_data)
        else:
            # TO DO
            print("Элемент <Товары> не найден")
