from datetime import timedelta
from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPAuthorizationCredentials, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException
import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from core.config import settings
from core.models.db_helper import db_helper
from .schemas import UserCreationModel, UserSchema, UserLoginModel
from .utils import create_access_token, check_password, create_refresh_token, decode_token
from .service import UserService
from .auth_handler import security
from typing import Annotated, List


auth_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@auth_router.post("/sign-up", status_code=status.HTTP_201_CREATED)
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


@auth_router.get(
    "/users", status_code=status.HTTP_200_OK, response_model=List[UserSchema]
)
async def get_all_users(session: AsyncSession = Depends(db_helper.session_getter)):
    users = await UserService(session).get_all_users()

    return users


@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(
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

    user = await UserService(session).get_user(username)

    if user is not None and check_password(password, user.hashed_password):
        access_token = create_access_token(
            data={
                "user_id": str(user.uid),
                "username": user.username,
                "role": user.role,
            }, 
            expires_delta=timedelta(minutes=settings.auth.access_token_expire_minutes),
        )

        refresh_token = create_refresh_token(
            data={
                "user_id": str(user.uid),
                "username": user.username,
                "role": user.role,
            }, 
            expires_delta=timedelta(minutes=settings.auth.refresh_token_expire_days),
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Email Or Password"
        )


@auth_router.post("/me", dependencies=[Depends(security)])
async def current_user(
    session: Annotated[
        AsyncSession, 
        Depends(db_helper.session_getter),
    ],
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, settings.auth.secret_key, algorithms=[settings.auth.algorithm])
        username = payload.get("username")
        if username is None:
            raise HTTPException(status_code=403, detail="Invalid token")
        user = await UserService(session).get_user(username)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=403, detail="Invalid token")


@auth_router.post("/refresh_token", status_code=status.HTTP_200_OK)
async def refresh_token(
    refresh_token: str, 
    session: Annotated[
        AsyncSession, 
        Depends(db_helper.session_getter),
    ],
):
    try:
        payload = jwt.decode(refresh_token, settings.auth.secret_key, algorithms=[settings.auth.algorithm])
        username = payload.get("username")
        if username is None:
            raise HTTPException(status_code=403, detail="Invalid refresh token")
        
        user = await UserService(session).get_user(username)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        new_access_token = create_access_token(
            data={
                "user_id": str(user.uid),
                "username": user.username,
                "role": user.role,
            }, 
            expires_delta=timedelta(minutes=settings.auth.access_token_expire_minutes),
        )
        return {"access_token": new_access_token, "token_type": "bearer"}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="Refresh token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=403, detail="Invalid refresh token")


@auth_router.post("/logout", status_code=status.HTTP_200_OK)
async def logout_users(
    session: Annotated[
        AsyncSession, 
        Depends(db_helper.session_getter),
    ],
    token: str = Depends(oauth2_scheme),
):
    payload = decode_token(token)
    if await UserService(session).add_token_to_blacklist(token=token, session=session):
        return {"msg": "Successfully logged out"}
    else:
        raise HTTPException(status_code=500, detail="Something went wrong")