from typing import Annotated
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.auth.validator import get_auth_user_from_token_of_type
from api.api_v1.auth.halper import REFRESH_TOKEN_TYPE
from core.models.db_helper import db_helper
from .schemas import TokenInfo, UserCreationModel
from api.api_v1.user.schemas import UserSchema
from .utils import decode_jwt, validate_auth_user
from .halper import create_access_token, create_refresh_token
from .validator import oauth2_scheme
from .service import UserService
from .auth_handler import security


router = APIRouter(tags=["auth"])


@router.post("/sign-up", status_code=status.HTTP_201_CREATED)
async def create_user_account(
    user_data: UserCreationModel, session: AsyncSession = Depends(db_helper.session_getter)
):
    email = user_data.email

    user = await UserService(session).get_user(email)

    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"error": "User Account Already Exists"},
        )
    else:
        new_user = await UserService(session).create_user(user_data)
        return {"message": "User Created successfully", "user": new_user}


@router.post("/login", response_model=TokenInfo, status_code=status.HTTP_200_OK)
async def login_user(
    user:UserSchema = Depends(validate_auth_user),
):
        access_token = create_access_token(user)
        refresh_token = create_refresh_token(user)

        return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
        )


@router.post(
    "/refresh_token", 
    response_model=TokenInfo,
    dependencies=[Depends(security)], 
    status_code=status.HTTP_200_OK,
    response_model_exclude_none=True,
)
async def auth_refresh_jwt(
    user: UserSchema = Depends(get_auth_user_from_token_of_type(REFRESH_TOKEN_TYPE)),
):
    access_token = create_access_token(user)
    
    return TokenInfo(
        access_token=access_token,
    )
    


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout_users(
    session: Annotated[
        AsyncSession, 
        Depends(db_helper.session_getter)
    ],
    token: str = Depends(oauth2_scheme),
):
    payload = decode_jwt(token)
    if await UserService(session).add_token_to_blacklist(token=token, session=session):
        return {"msg": "Successfully logged out"}
    else:
        raise HTTPException(status_code=500, detail="Something went wrong")
    


