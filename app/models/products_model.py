from datetime import datetime
from typing import Optional
from typing_extensions import Annotated
from pydantic import BaseModel, BeforeValidator, Field


PyObjectId = Annotated[str, BeforeValidator(str)]

class Product(BaseModel):
    title: str
    image_url:str
    description: str
    quantity: int
    price: float

    
class CreateProduct(Product):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    created_at: datetime = datetime.now()


class UpdateProduct(Product):
    updated_at: datetime = datetime.now()


class ViewProduct(Product):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    created_at: datetime 
    updated_at: datetime | None = None
