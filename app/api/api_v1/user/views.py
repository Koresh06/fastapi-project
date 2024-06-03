from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from api.api_v1.auth.utils import get_current_user
from core.models import User

from core.models import db_helper



router = APIRouter(
    tags=["users"]
)


@router.get("/", status_code=status.HTTP_200_OK)
async def user(
    user: Annotated[
        dict, 
        Depends(get_current_user)
    ],
    session: Annotated[
        AsyncSession, 
        Depends(db_helper.session_getter)
    ],
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication Failed",
        )
    return {"User": user}
