from fastapi import APIRouter, HTTPException, Depends
from auth import auth
from models import User, Token
from datetime import datetime, timedelta
import os

router = APIRouter(
    prefix='/users',
    tags=['users'],
    responses={
        404: {"description": "Not Found"},
        401: {"description": "Not authenticated"},
        400: {"description": "Bad Request"},
        403: {"description": "Forbidden"}
    }
)


# password for umutaev is "samara"
@router.post('/login', response_model=Token.Model)
async def serve_users(credentials: User.LoginModel) -> Token:
    user = await auth.authentication(
        credentials.username, credentials.plain_password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Wrong credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = await auth.create_access_token(
        data={"sub": str(user.id)},  expires_delta=timedelta(minutes=1)
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get('/me', response_model=User.ReturnModel)
async def serve_me(current_user=Depends(auth.get_current_user)):
    return current_user


@router.post('/new', response_model=Token.Model)
async def serve_signup(user: User.SignUpModel):
    return await auth.create_new_user(user)
