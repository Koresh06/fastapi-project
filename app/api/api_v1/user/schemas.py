from pydantic import BaseModel, ConfigDict, EmailStr
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")




