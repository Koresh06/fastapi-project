from typing import List
from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.user.schemas import UserSchema, UserUpdateModel
from api.api_v1.user.service import UserService
from api.api_v1.user.dependencies import user_by_uid
from core.models import db_helper
from api.api_v1.auth.dependencies import RolesChecker, get_current_user


router = APIRouter(
    tags=["users"],
)


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user: UserSchema = Depends(user_by_uid),
    session: AsyncSession = Depends(db_helper.session_getter),
    _: bool = Depends(RolesChecker(["admin"])),
):
    await UserService(session).delete_user(user=user)

    return JSONResponse(
        content={
            "message": f"Delete user - {user.username}"
        },
        status_code=status.HTTP_200_OK
    )


@router.patch("/update", status_code=status.HTTP_200_OK, response_model=UserSchema)
async def update_user(
    user_update: UserUpdateModel,
    user: UserSchema = Depends(user_by_uid),
    session: AsyncSession = Depends(db_helper.session_getter),
    _: bool = Depends(RolesChecker(["admin"])),
):
    return await UserService(session).update_user(
        user=user, 
        user_update=user_update, 
        partil=True
    )


@router.get("/get", status_code=status.HTTP_200_OK, response_model=UserSchema)
async def get_user(
    user: UserSchema = Depends(user_by_uid),
    session: AsyncSession = Depends(db_helper.session_getter),
    _: bool = Depends(RolesChecker(["admin"])),
):
    return user
    

@router.get("/get_all", status_code=status.HTTP_200_OK, response_model=List[UserSchema])
async def get_all_users(
    session: AsyncSession = Depends(db_helper.session_getter),
    _: bool = Depends(RolesChecker(["admin"])),
    limit: int = Query(default=10, ge=1),  
    offset: int = Query(default=0, ge=0)   
):
    users = await UserService(session).get_all_users(limit=limit, offset=offset)
    return users


@router.get("/me", status_code=status.HTTP_200_OK, response_model=UserSchema)
async def current_user(
    _: bool = Depends(RolesChecker(["admin"])),
    user: dict = Depends(get_current_user),

):
    return user