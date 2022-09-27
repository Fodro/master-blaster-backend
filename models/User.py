from pydantic import BaseModel
class Model(BaseModel):
	id: int
	username: str
	email: str
	hashed_password: str

class LoginModel(BaseModel):
	username: str
	plain_password: str
