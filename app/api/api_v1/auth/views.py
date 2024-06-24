from fastapi import APIRouter, Depends, status

from core.models.user import User
from .schemas import UserCreateModel, UserModel, UserLoginModel
from .service import AuthUserService
from core.models.db_helper import db_helper
from sqlalchemy.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from .utils import create_access_token, verify_password
from fastapi.responses import JSONResponse
from datetime import timedelta, datetime
from .dependencies import RefreshTokenBearer,AccessTokenBearer, RolesChecker
from core.redis import add_jti_to_blocklist


auth_router = APIRouter(
    tags=["auth"],
)

REFRESH_TOKEN_EXPIRY = 2


@auth_router.post(
    "/signup", response_model=UserModel, status_code=status.HTTP_201_CREATED
)   
async def create_user_Account(
    user_data: UserCreateModel, 
    session: AsyncSession = Depends(db_helper.session_getter),
):
    email = user_data.email

    user_exists = await AuthUserService(session).user_exists(email)

    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User with email already exists",
        )

    new_user = await AuthUserService(session).create_user(user_data)

    return new_user


@auth_router.post("/login")
async def login_users(
    login_data: UserLoginModel, session: AsyncSession = Depends(db_helper.session_getter)
):
    email = login_data.email
    password = login_data.password

    user: User = await AuthUserService(session).get_user_by_email(email)

    if user is not None:
        password_valid = verify_password(password, user.hashed_password)

        if password_valid:
            access_token = create_access_token(
                user_data={"email": user.email, "user_uid": str(user.uid), "role": user.role}
            )

            refresh_token = create_access_token(
                user_data={"email": user.email, "user_uid": str(user.uid), "role": user.role},
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY),
            )

            return JSONResponse(
                content={
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {"email": user.email, "uid": str(user.uid), "role": user.role},
                }
            )

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Email Or Password"
    )


@auth_router.get("/refresh_token")
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details["exp"]

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(user_data=token_details["user"])

        return JSONResponse(content={"access_token": new_access_token})

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Or expired token"
    )


@auth_router.get('/logout')
async def revoke_token(token_details: dict = Depends(AccessTokenBearer())):

    jti = token_details['jti']

    await add_jti_to_blocklist(jti)

    return JSONResponse(
        content={
            "message":"Logged Out Successfully"
        },
        status_code=status.HTTP_200_OK
    )