from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request, status, Depends
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from api.api_v1.auth.service import AuthUserService

from core.models.user import User
from .utils import decode_token
from fastapi.exceptions import HTTPException
from core.redis import token_in_blocklist
from core.models.db_helper import db_helper

class TokenBearer(HTTPBearer):

    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)

        token = creds.credentials

        token_data = decode_token(token)

        if not self.token_valid:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or expired token"
            )
        
        if await token_in_blocklist(token_data['jti']):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail={
                    "error":"This token is invalid or has been revoked",
                    "resolution":"Please get new token"
                }
            )
        
        self.verify_token_data(token_data)

        return token_data

    def token_valid(self, token: str) -> bool:

        token_data = decode_token(token)

        return token_data is not None 
    
    def verify_token_data(self, token_data):
        raise NotImplementedError("Please Override this method in child classes")


class AccessTokenBearer(TokenBearer):

    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide an access token",
            )


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide a refresh token",
            )


async def get_current_user(
        token_details: dict = Depends(AccessTokenBearer()),
        session: AsyncSession = Depends(db_helper.session_getter),
):
    user_email = token_details["user"]["email"]
    user = await AuthUserService(session).get_user_by_email(user_email)

    return user


class RolesChecker:

    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)):
        if current_user.role in self.allowed_roles:
            return True
        
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='У вас нет доступа к этому ресурсу'
        )