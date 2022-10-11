from code import interact
from pydantic import BaseModel
from typing import Optional


class Model(BaseModel):
    username: Optional[str]
