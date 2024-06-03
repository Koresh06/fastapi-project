from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import CreateUserRequest, Token
from .utils import create_access_token
from .crud import authenticate_user, bcrypt_context
from core.models import db_helper
from core.models import User
from core.config import settings


router = APIRouter(
    tags=["auth"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(
    create_user_request: CreateUserRequest,
    session: Annotated[
        AsyncSession, 
        Depends(db_helper.session_getter),
    ],
):
    create_user_model = User(
        username=create_user_request.username,
        email=create_user_request.email,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password),
    )

    session.add(create_user_model)
    await session.commit()


@router.post("/logout", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[
        AsyncSession, 
        Depends(db_helper.session_getter),
    ],
):
    user = await authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    token = await create_access_token(
        user.username,
        str(user.id),
        user.role,
        timedelta(minutes=settings.auth.access_token_expire_minutes),
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }


   