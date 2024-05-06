from typing import Optional
from typing_extensions import Annotated
from pydantic import BaseModel, BeforeValidator, Field


PyObjectId = Annotated[str, BeforeValidator(str)]

class User(BaseModel):
    username: str
    password: str


class UserInDB(User):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    hashed_password: str


class ResponseUserInDB(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    username: str
    hashed_password: str