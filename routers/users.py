from fastapi import APIRouter, HTTPException, Depends, Request
from db import users
from auth import auth
from models import User, Token


router = APIRouter(
	prefix='/users',
	tags=['users'],
	responses={
		404: {"description": "Not Found"},
		400: {"description": "Bad Request"},
		403: {"description": "Forbidden"}
	}
)




@router.post('/login', response_model=Token.Model) #password for umutaev is "samara"
def serve_users(credentials: User.LoginModel) -> Token:
	user = auth.authentication(credentials.username, credentials.plain_password)
	if not user:
		raise HTTPException(
            status_code=401,
            detail="Wrong credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
	# access_token_expires = timedelta(os.environ["ACCESS_TOKEN_EXPIRATION_TIME"])
	access_token = auth.create_access_token(
		data={"user_id": user.id}, # expires_delta=access_token_expires
	)
	return{"access_token": access_token, "token_type": "bearer"}

@router.get('/me', dependencies=[Depends(auth.JWTBearer())],)
def serve_me(request: Request):
	return auth.get_current_user(request.headers["authorization"][7:])