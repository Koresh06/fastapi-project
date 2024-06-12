import uuid
import jwt
from typing import Annotated
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.auth.service import UserService
from api.api_v1.auth.password_utils import check_password
from core.models import db_helper
from core.config import settings


SECRET_KEY = settings.auth.secret_key
ALGORITHM = settings.auth.algorithm


def encode_jwt(
    payload: dict,
    secret_key: str = settings.auth.secret_key,
    algorithm: str = settings.auth.algorithm,
    expire_minutes: int = settings.auth.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
) -> str:
    to_encode = payload.copy()
    now = datetime.utcnow()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now,
        jti=str(uuid.uuid4()),
    )
    encoded = jwt.encode(
        to_encode,
        secret_key,
        algorithm=algorithm,
    )
    return encoded


def decode_jwt(
    token: str | bytes,
    secret_key: str = settings.auth.secret_key,
    algorithm: str = settings.auth.algorithm,
) -> dict:
    decoded = jwt.decode(
        token,
        secret_key,
        algorithms=[algorithm],
    )
    return decoded


async def validate_auth_user(
    form_data: Annotated[
        OAuth2PasswordRequestForm, 
            Depends(),
    ],
    session: Annotated[
        AsyncSession, 
        Depends(db_helper.session_getter),
    ],
):
    username = form_data.username
    password = form_data.password

    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
    )

    if not (user := await UserService(session).get_user(username)):
        raise unauthed_exc

    if not check_password(password, user.hashed_password):
        raise unauthed_exc

    if user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user inactive",
        )

    return user
