from typing import Annotated
from fastapi import APIRouter, Path
from common.schema import PaginatedData
from common.security.header import DependsHeader
from common.security.jwt import DependsJwtAuth

from common.pagination import DependsPagination, paging_data
from common.response.response_schema import ResponseModel, response_base

from app.user.schema.object import GetObjectInfoListDetails, GetObjectInfoDetails
from app.user.schema.product import GetProductInfoListDetails, GetProductInfoDetails
from app.user.schema.smart import CreateSmart
from database.db_postgres import CurrentSession

from app.user.service.bitrix_service import bitrix_service
from app.user.service.object_srvice import object_service
from app.user.service.product_srvice import product_service
from utils.serializers import select_as_dict


router = APIRouter(prefix="/b24", tags=["Api Bitrix"])


@router.post(
    "/create_smart",
    response_model=ResponseModel[CreateSmart],
    summary="Сознание smart процесса в bitrix ",
    description="",
    dependencies=[DependsJwtAuth],
)
async def create_smart(response_model: CreateSmart) -> ResponseModel:
    data = await bitrix_service.create_smart(response_model)
    return response_base.success(data=data)


@router.get(
    "/get_objects",
    response_model=ResponseModel[PaginatedData[GetObjectInfoListDetails]],
    summary="Получение Объектов из bitrix",
    description="Получение списка всех объектов с адресами",
    dependencies=[DependsHeader, DependsJwtAuth, DependsPagination],
)
async def get_pagination_objects(db: CurrentSession) -> ResponseModel:
    object_select = await object_service.get()
    page_data = await paging_data(db, object_select, GetObjectInfoListDetails)
    return response_base.success(data=page_data)


@router.get(
    "/get_object/{object_id}",
    response_model=ResponseModel[GetObjectInfoDetails],
    summary="Получение Объекта по id",
    description="",
    dependencies=[DependsJwtAuth],
)
async def get_object(
    object_id: Annotated[int, Path(...)]
) -> ResponseModel[GetObjectInfoDetails]:
    object_select = await object_service.get_select(object_id=object_id)
    data = GetObjectInfoDetails(**select_as_dict(object_select))
    return response_base.success(data=data)


@router.get(
    "/search_object",
    response_model=ResponseModel[PaginatedData[GetObjectInfoListDetails]],
    summary="Получение Объектов из bitrix",
    description="Получение списка всех объектов с адресами",
    dependencies=[DependsPagination],
)
async def search_object(db: CurrentSession, query: str) -> ResponseModel:
    object_select = await object_service.search_object(query=query)
    page_data = await paging_data(db, object_select, GetObjectInfoListDetails)
    return response_base.success(data=page_data)


@router.get(
    "/get_products",
    response_model=ResponseModel[PaginatedData[GetProductInfoListDetails]],
    summary="Получение продуктов из 1c",
    description="Получение списка всех продуктов",
    dependencies=[DependsJwtAuth, DependsPagination],
)
async def get_pagination_products(db: CurrentSession) -> ResponseModel:
    product_select = await product_service.get()
    page_data = await paging_data(db, product_select, GetProductInfoListDetails)
    return response_base.success(data=page_data)


@router.get(
    "/get_product/{product_id}",
    response_model=ResponseModel[GetProductInfoDetails],
    summary="Получение Продукта по id",
    description="",
    dependencies=[DependsJwtAuth],
)
async def get_product(
    product_id: Annotated[int, Path(...)]
) -> ResponseModel[GetProductInfoDetails]:
    product_select = await product_service.get_select(product_id=product_id)
    data = GetProductInfoDetails(**select_as_dict(product_select))
    return response_base.success(data=data)


@router.get(
    "/search_product",
    response_model=ResponseModel[PaginatedData[GetProductInfoListDetails]],
    summary="Поиск продуктов из bitrix",
    description="Получение списка продуктов с адресами по заданной строке поиска",
    dependencies=[DependsJwtAuth, DependsPagination],
)
async def search_product(db: CurrentSession, query: str) -> ResponseModel:
    product_select = await product_service.search_product(query=query)
    page_data = await paging_data(db, product_select, GetProductInfoListDetails)
    return response_base.success(data=page_data)


@router.get(
    "/get_products_with_quantity",
    response_model=ResponseModel[PaginatedData[GetProductInfoListDetails]],
    summary="Получение продуктов с остатком болше 0",
    description="Получение списка продуктов с остатком болше 0",
    dependencies=[DependsJwtAuth, DependsPagination],
)
async def get_pagination_products_with_quantity(db: CurrentSession) -> ResponseModel:
    product_select = await product_service.get_select_with_quantity()
    page_data = await paging_data(db, product_select, GetProductInfoListDetails)
    return response_base.success(data=page_data)


@router.get(
    "/search_products_with_quantity",
    response_model=ResponseModel[PaginatedData[GetProductInfoListDetails]],
    summary="Поиск продуктов из 1C с остатком болше 0",
    description="Получение списка продуктов с адресами по заданной строке поиска с остатком болше 0",
    dependencies=[DependsJwtAuth, DependsPagination],
)
async def search_products_with_quantity(
    db: CurrentSession, query: str
) -> ResponseModel:
    product_select = await product_service.search_product_with_quantity(query=query)
    page_data = await paging_data(db, product_select, GetProductInfoListDetails)
    return response_base.success(data=page_data)
