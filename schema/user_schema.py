from pydantic import BaseModel
from typing import Optional


class UserSchema(BaseModel):
    id: Optional[str]
    name: str
    username: str
    password: str


class DataUser(BaseModel):
    username: str
    password: str
