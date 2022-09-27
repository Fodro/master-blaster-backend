from pydantic import BaseModel
from typing import Optional
class Model(BaseModel):
	user_id: Optional[str]