from typing import Annotated
from jwt import InvalidTokenError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.auth import utils
from api.api_v1.user.schemas import UserSchema
from api.api_v1.auth.halper import TOKEN_TYPE_FIELD, ACCESS_TOKEN_TYPE
from api.api_v1.user.service import UserService
from core.models import db_helper


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_token_payload(
    token: str = Depends(oauth2_scheme),
) -> dict:
    try:
        payload = utils.decode_jwt(
            token=token,
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error: {e}",
        )
    return payload


def validate_token_type(
    payload: dict,
    token_type: str,
) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"invalid token type {current_token_type!r} expected {token_type!r}",
    )


async def get_user_by_token_sub(
        payload: dict, 
        session: Annotated[
            AsyncSession, 
            Depends(db_helper.session_getter),
        ],
    ) -> UserSchema:
    username: str | None = payload.get("username")
    if user := await UserService(session).get_user(username):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid (user not found)",
    )


def get_auth_user_from_token_of_type(token_type: str):
    async def get_auth_user_from_token(
        session: Annotated[
            AsyncSession, 
            Depends(db_helper.session_getter),
        ],   
        payload: dict = Depends(get_current_token_payload),
    ) -> UserSchema:
        validate_token_type(payload, token_type)
        return await get_user_by_token_sub(payload, session)

    return get_auth_user_from_token


async def get_current_active_auth_user(
    user: UserSchema = Depends(get_auth_user_from_token_of_type(ACCESS_TOKEN_TYPE)),
):
    if not user.is_verified:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="inactive user",
    )