from typing import Optional
from typing_extensions import Annotated
from pydantic import BaseModel, BeforeValidator, Field

PyObjectId = Annotated[str, BeforeValidator(str)]

class Token(BaseModel):
    acces_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    password: str
    disabled: bool | None = None


class UserInDB(User):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    hashed_password: str
