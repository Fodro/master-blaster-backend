#TODO adapt to async after db connection

from passlib.context import CryptContext
from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from datetime import timedelta, datetime
from models import TokenData, User
from db import users

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "changemeintoenvvar" #TODO change this to env after dev
ALGORITHM = "HS256"

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            data = self.verify_jwt(credentials.credentials)
            if not data:
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return data
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, token: str) -> bool:
        is_token_valid: bool = False

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except:
            data = None
        if data:
            is_token_valid = True
        return is_token_valid

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)

def authentication(username: int, password: str) -> User.Model:
    user = users.get_user_by_username(username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=403, detail="Wrong credentials")
    return user

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=3)) -> str: # DO NOT USE DEFAULT VALUE
    data_to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    data_to_encode.update({"expires": expire.strftime("%Y-%m-%d %H:%M:%S")})
    encoded_jwt = jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str) -> User.Model:
    data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return users.get_user_by_id(data['user_id'])

