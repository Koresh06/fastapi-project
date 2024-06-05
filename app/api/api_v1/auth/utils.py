from datetime import datetime, timedelta
from fastapi import HTTPException

import jwt
from passlib.context import CryptContext

from core.config import settings

PASSWORD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = settings.auth.secret_key
ALGORITHM = settings.auth.algorithm



def check_password(plain_password: str, hashed_password: str) -> bool:
    """Check and verify your password against a hash"""
    return PASSWORD_CONTEXT.verify(plain_password, hashed_password)


def create_password_hash(plain_password: str) -> str:
    """Hash a password to be stored in the database"""
    return PASSWORD_CONTEXT.hash(plain_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Create new access token for authorization"""
    data = data.copy()

    now = datetime.now()

    if not expires_delta:
        expires_delta = timedelta(minutes=30)

    data.update({"exp": now + expires_delta})

    token = jwt.encode(data, SECRET_KEY, ALGORITHM)

    return token


def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=7)  # Рефреш-токен действует 7 дней
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_user_from_jwt(token: str) -> str | None:
    """Get user from  a given JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if not (username := payload.get("sub")):
            return None

    except jwt.PyJWTError:
        return None

    return username

