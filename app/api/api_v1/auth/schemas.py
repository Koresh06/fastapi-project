from pydantic import BaseModel, EmailStr


class CreateUserRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str

    # model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str