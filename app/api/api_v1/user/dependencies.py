from typing import Annotated
import uuid
from fastapi import Depends, HTTPException, status, Path
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.user.service import UserService
from core.models.user import User
from core.models import db_helper


async def user_by_uid(
    user_uid: Annotated[uuid.UUID, Path],
    session: AsyncSession = Depends(db_helper.session_getter),
) -> User:
    user = await UserService(session).get_user_uid(user_uid)
    if user is not None:
        return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User {user_uid} not found!",
    )