# TODO adapt to async after db connection

from passlib.context import CryptContext
from fastapi import HTTPException, Depends
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta, datetime
from models import TokenData, User
from db import users

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "changemeintoenvvar"  # TODO change this to env after dev
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


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


# DO NOT USE DEFAULT VALUE
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=3)) -> str:
    data_to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    data_to_encode.update({"expires": expire.strftime("%Y-%m-%d %H:%M:%S")})
    encoded_jwt = jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = int(data.get("sub"))
        if user_id is None:
            raise credentials_exception
        token_data = TokenData.Model(user_id=user_id)
    except JWTError:
        raise credentials_exception
    user = users.get_user_by_username(token_data.user_id)
    if user is None:
        raise credentials_exception
    return user
