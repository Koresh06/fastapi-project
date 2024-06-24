import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserCreateModel(BaseModel):
    
    username: str
    email: EmailStr
    hashed_password: str


class UserModel(BaseModel):

    uid: uuid.UUID
    username: str
    email: EmailStr
    created_at: datetime



class UserLoginModel(BaseModel):

    email: EmailStr
    password: str