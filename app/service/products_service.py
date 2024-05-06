from typing import List
from bson import ObjectId
from fastapi import HTTPException, status

from app.core.database import db
from app.models.products_model import Product, CreateProduct, UpdateProduct, ViewProduct


class ProductSerice:

    product_collection = db.get_collection('products')
    
    async def create_new_product(self, product: Product) -> ViewProduct:
        db_request = CreateProduct(**product.model_dump(exclude_none=True))
        request = await self.product_collection.insert_one(db_request.model_dump(by_alias=True, exclude=["id"]))
        
        final_request = await self.product_collection.find_one(
            {"_id":request.inserted_id}
        )
        return final_request
    
    
    async def get_list_of_products(self, limit: int) -> List[ViewProduct]:
        return await self.product_collection.find().to_list(limit)
    
    async def find_product_by_id(self, id: str) -> ViewProduct:
            data = await self.product_collection.find_one({'_id':ObjectId(id)})
            if not data:
                raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"product id: {id}, not found"
            )   
            return data


    async def update_product_by_id(self,id: str, product: Product) -> UpdateProduct:
        data = await self.product_collection.find_one({'_id':ObjectId(id)})
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"product id: {id}, not found"
            )
        
        update_product = UpdateProduct(**product.model_dump(exclude_none=True))
        update_request = await self.product_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": update_product.model_dump(by_alias=True)}
        )
        if update_request is not None:
            return update_request
        else:
            raise HTTPException(status_code=404, detail=f"Product {id} not found")


    async def pop_porduct_off_the_storage(self, id:str, quantity: int):
        data = await self.product_collection.find_one({'_id':ObjectId(id)})
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"product id: {id}, not found"
            )

        pre_stage = await self.product_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            { "$inc": { 'quantity': -quantity } }
        )
        return_data = await self.product_collection.find_one({'_id':ObjectId(id)})
        if return_data is not None:
            return return_data
        else:
            raise HTTPException(status_code=404, detail=f"Product {id} not found")
        
    async def delete_product_by_id(self, id:str) -> None:
        data = await self.product_collection.find_one({'_id':ObjectId(id)})
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"product id: {id}, not found"
            )
        
        try:
            await self.product_collection.find_one_and_delete({'_id':ObjectId(id)})
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f'Error: {e}'
            )