from pydantic import BaseModel
class Model(BaseModel):
	access_token: str
	token_type: str