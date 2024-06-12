from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.user.schemas import UserSchema
from api.api_v1.auth.auth_handler import security
from api.api_v1.auth.validator import get_auth_user_from_token_of_type, get_current_active_auth_user
from api.api_v1.auth.service import UserService
from api.api_v1.auth.halper import ACCESS_TOKEN_TYPE
from core.models import db_helper


router = APIRouter(
    tags=["users"],
    dependencies=[Depends(security)]
)


@router.get("/get_all", status_code=status.HTTP_200_OK, response_model=List[UserSchema])
async def get_all_users(
    user: UserSchema = Depends(get_current_active_auth_user),  # Проверка текущего активного пользователя
    session: AsyncSession = Depends(db_helper.session_getter),
):
    users = await UserService(session).get_all_users()
    return users


@router.get("/me", status_code=status.HTTP_200_OK, response_model=UserSchema)
async def current_user(
    # payload: dict = Depends(get_current_token_payload),
    user: UserSchema = Depends(get_auth_user_from_token_of_type(ACCESS_TOKEN_TYPE)),
):
    # iat = payload.get("iat")
    return user