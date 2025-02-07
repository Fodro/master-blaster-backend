from passlib.context import CryptContext
from fastapi import HTTPException, Depends
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta, datetime
from models import TokenData, User, Token
from db.users import UsersDB
import logging
import os

logging.basicConfig(level=logging.INFO)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = str(os.environ.get('SECRET_KEY'))
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
users_db = UsersDB()


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


async def authentication(username: int, password: str) -> User.Model:
    logging.info("Authentication inited")
    user = await users_db.get_user_by_username(username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not await verify_password(password, user.hashed_password):
        raise HTTPException(status_code=403, detail="Wrong credentials")
    return user


async def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=3)) -> str:
    logging.info("Creating access token")
    data_to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    data_to_encode.update({"expires": expire.strftime("%Y-%m-%d %H:%M:%S")})
    encoded_jwt = jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User.Model:
    logging.info("Getting current user")
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_exception = HTTPException(
        status_code=401,
        detail="Token expired",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = data.get("sub")
        expiration_time: datetime = datetime.strptime(
            data.get("expires"), "%Y-%m-%d %H:%M:%S")
        if expiration_time <= datetime.utcnow():
            raise token_exception
        if username is None:
            raise credentials_exception
        token_data = TokenData.Model(username=username)
    except JWTError:
        raise credentials_exception
    user = await users_db.get_user_by_username(token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def create_new_user(user: User.SignUpModel) -> Token.Model:
    logging.info("Crearing new user")
    hashed_password = await hash_password(user.plain_password)
    new_user = await users_db.create_new_user(User.Model(id=1, username=user.username,
                                                         email=user.email, hashed_password=hashed_password))
    access_token = await create_access_token(
        data={"sub": str(new_user.username)}, expires_delta=timedelta(days=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}
