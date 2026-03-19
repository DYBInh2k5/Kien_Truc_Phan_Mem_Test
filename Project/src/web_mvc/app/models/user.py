# app/models/user.py
from pydantic import BaseModel
from typing import Optional

class UserLogin(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    username: str
    password: str
    email: str

class User(BaseModel):
    id: int
    username: str
    email: str
    is_admin: bool = False
