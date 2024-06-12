from pydantic import BaseModel, EmailStr


class TokenInfo(BaseModel):
    
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


class UserCreationModel(BaseModel):

    username: str
    email: EmailStr
    hashed_password: str
    role: str
