import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):

    uid: uuid.UUID
    username: str
    email: EmailStr
    role: str
    is_verified: bool
    created_at: datetime


