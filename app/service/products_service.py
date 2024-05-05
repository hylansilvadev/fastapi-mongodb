from typing import List
from bson import ObjectId
from fastapi import HTTPException, status

from app.core.database import db
from app.models.products_model import Product, CreateProduct, UpdateProduct, ViewProduct

product_collection = db.get_collection('products')

class ProductSerice:
    
    async def create_new_product(self, product: Product) -> ViewProduct:
        db_request = CreateProduct(**product.model_dump(exclude_none=True))
        request = await product_collection.insert_one(db_request.model_dump(by_alias=True, exclude=["id"]))
        
        final_request = await product_collection.find_one(
            {"_id":request.inserted_id}
        )
        return final_request
    
    
    async def get_list_of_products(self, limit: int) -> List[ViewProduct]:
        return await product_collection.find().to_list(limit)
    
    async def find_product_by_id(self, id: str) -> ViewProduct:
            data = await product_collection.find_one({'_id':ObjectId(id)})
            if not data:
                raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"product id: {id}, not found"
            )   
            return data


    async def update_product_by_id(self,id: str, product: Product):
        data = await product_collection.find_one({'_id':ObjectId(id)})
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"product id: {id}, not found"
            )
        
        update_product = UpdateProduct(**product.model_dump(exclude_none=True))
        update_request = await product_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": update_product.model_dump(by_alias=True)}
        )
        if update_request is not None:
            return update_request
        else:
            raise HTTPException(status_code=404, detail=f"Student {id} not found")