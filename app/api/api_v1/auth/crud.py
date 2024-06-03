from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext

from core.models.user import User


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def authenticate_user(
        username: str, 
        password: str, 
        session: AsyncSession
) -> User | None:
    user = await session.scalar(select(User).where(User.username == username))
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user