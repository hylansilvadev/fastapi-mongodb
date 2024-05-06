import pytz
from datetime import datetime
from typing import Optional
from typing_extensions import Annotated
from pydantic import BaseModel, BeforeValidator, Field


PyObjectId = Annotated[str, BeforeValidator(str)]

local_tz = pytz.timezone('America/Sao_Paulo')

class Product(BaseModel):
    title: str
    image_url:str
    description: str
    quantity: int
    price: float

    
class CreateProduct(Product):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    created_at: datetime = datetime.now(local_tz)


class UpdateProduct(Product):
    updated_at: datetime = datetime.now(local_tz)


class ViewProduct(Product):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    created_at: datetime 
    updated_at: datetime | None = None
