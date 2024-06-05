import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserCreationModel(BaseModel):
    """Model for user creation"""
    username: str
    email: EmailStr
    hashed_password: str
    role: str


class UserSchema(BaseModel):
    """General user information model"""
    uid: uuid.UUID
    username: str
    email: EmailStr
    role: str
    is_verified: bool
    created_at: datetime


class UserLoginModel(BaseModel):
    """A model for logging a user in to get an access token"""
    email: EmailStr
    hashed_password: str