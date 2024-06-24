from passlib.context import CryptContext
from datetime import timedelta, datetime
from core.config import settings
import jwt
import uuid
import logging

passwd_context = CryptContext(schemes=["bcrypt"])


ACCESS_TOKEN_EXPIRY = 3600


def generate_passwd_hash(password: str) -> str:
    hash = passwd_context.hash(password)

    return hash


def verify_password(password: str, hash: str) -> bool:
    return passwd_context.verify(password, hash)


def create_access_token(user_data: dict, expiry: timedelta = None, refresh: bool= False):
    payload = {}

    payload["user"] = user_data
    payload["exp"] = datetime.now() + (
        expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY)
    )
    payload['jti'] = str(uuid.uuid4())

    payload['refresh'] = refresh


    token = jwt.encode(
        payload=payload, key=settings.auth.secret_key, algorithm=settings.auth.algorithm
    )

    return token


def decode_token(token: str) -> dict:
    try:
        token_data = jwt.decode(
            jwt= token,
            key=settings.auth.secret_key,
            algorithms=[settings.auth.algorithm],
        )

        return token_data
    
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None