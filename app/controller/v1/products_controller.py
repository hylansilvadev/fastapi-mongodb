from typing import List
from typing_extensions import Annotated
from fastapi import APIRouter, Depends, HTTPException, status

from app.models.products_model import Product, ViewProduct
from app.service.products_service import ProductSerice
from app.core.security import Security


router = APIRouter(
    prefix='/products',
    tags=["Products"]
)

sec = Security()

product_service = ProductSerice()

@router.post(
    '/',
    response_model=ViewProduct,
    response_model_by_alias=False,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(sec.get_current_user)]
)

async def create_new_product(data: Product):
        request = await product_service.create_new_product(data)
        return request


@router.get(
    '/',
    response_model=List[ViewProduct],
    response_model_by_alias=False,
    status_code=status.HTTP_200_OK,
)
async def get_list_of_products(limit: int = 1000):
        request = await product_service.get_list_of_products(limit)
        return request


@router.get(
    '/{id}',
    response_model=ViewProduct,
    response_model_by_alias=False,
    status_code=status.HTTP_200_OK
)
async def get_list_of_products(id: str):
        request = await product_service.find_product_by_id(id)
        return request


@router.put(
    '/{id}',
    response_model=ViewProduct,
    response_model_by_alias=False,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(sec.get_current_user)]
)
async def update_product_by_id(id: str, product:Product):
    request = await product_service.update_product_by_id(id, product)
    return request


@router.patch(
    '/{id}',
    response_model=ViewProduct,
    response_model_by_alias=False,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(sec.get_current_user)]
)
async def pop_porduct_off_the_storage_by_id(id: str, quantity:int):
    request = await product_service.pop_porduct_off_the_storage(id, quantity)
    return request


@router.delete(
    '/{id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(sec.get_current_user)]
)
async def delete_product_by_id(id: str):
    await product_service.delete_product_by_id(id)