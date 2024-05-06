import pytz
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status, APIRouter
from typing_extensions import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.models.seccurity_models import TokenData, User, UserInDB, Token, ResponseUserInDB
from app.core.config import settings
from app.core.database import db


router = APIRouter(prefix='/auth', tags=['Authentication'])

class Security:
    local_tz = pytz.timezone('America/Sao_Paulo')
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
    user_collection = db.get_collection("users")
    
    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password,hashed_password)
    

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)


    async def get_user(self, username:str):
        user = await self.user_collection.find_one({"username":username})
        if user:
            return ResponseUserInDB(**user)


    async def authenticate_user(self, username: str, password: str):
        user = await self.get_user(username)
        if not user:
            return False
        if not self.verify_password(password, user.hashed_password):
            return False
        return user


    def create_access_token(self, username:str, user_id:str, expires_delta: timedelta | None = None):
        encode = {'sub':username, 'id':user_id}
        expires = datetime.now(self.local_tz) + timedelta(minutes=expires_delta)
        encode.update({'exp': expires})
        return jwt.encode(encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)



    async def get_current_user(self, token: Annotated[str, Depends(oauth2_scheme)]):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError as e:
            print(f'JWTError: {e}')
            raise credentials_exception
        user = self.get_user( username=token_data.username)
        if user is None:
            raise credentials_exception
        return user


    async def get_current_active_user(self, current_user: Annotated[User, Depends(get_current_user)]):
        if current_user.disabled:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user
    
    

sec = Security()

@router.post('/')
async def create_new_user(user:User):
        user_create_model = UserInDB(**user.model_dump(exclude_none=True), hashed_password=sec.pwd_context.hash(user.password))
        try: 
            await sec.user_collection.insert_one(user_create_model.model_dump(exclude=["password", "id"]))
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f'{e}'
            )
    
@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = await sec.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = sec.create_access_token(
    username=user.username, user_id=user.id, expires_delta=settings.ACCESS_TOKEN_EXPIRE_MINUTES
)
    return Token(access_token=access_token, token_type="bearer")