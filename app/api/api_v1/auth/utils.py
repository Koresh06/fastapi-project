from datetime import datetime, timedelta
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from core.models import db_helper

from core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")



async def create_access_token(
    username: str,
    user_id: str,
    role: str,
    expires_delta: timedelta,
):
    encode = {"sub": username, "id": user_id, "role": role}
    expires = datetime.utcnow() + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, settings.auth.secret_key, algorithm=settings.auth.algorithm)
    

async def get_current_user(
    token: Annotated[
        str, 
        Depends(oauth2_scheme)
    ],
    session: Annotated[
        AsyncSession, 
        Depends(db_helper.session_getter),
    ],
):
    try:
        payload = jwt.decode(token, settings.auth.secret_key, algorithms=[settings.auth.algorithm])
        username: str = payload.get("sub")
        user_id: str = str(payload.get("id"))
        role: str = payload.get("role")
        if username is None or user_id is None or role is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
        return {"username": username, "id": user_id, "role": role}
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )