from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import User

from core.models import db_helper


router = APIRouter(
    tags=["users"]
)


# @router.get("/users/me", status_code=status.HTTP_200_OK)
# async def user(
#     user: Annotated[
#         dict, 
#         Depends(get_current_active_user)
#     ],
#     session: Annotated[
#         AsyncSession, 
#         Depends(db_helper.session_getter)
#     ],
# ):
#     if user is None:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Authentication Failed",
#         )
#     if user.role != 'admin':
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User is not admin')
#     return {"User": user}
