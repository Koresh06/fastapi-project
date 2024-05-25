from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result
from .schemas import UserCreate

from core.models import User


async def get_all_users(session: AsyncSession) -> Sequence[User]:
    stmt = select(User).order_by(User.id)
    result: Result = await session.scalars(stmt)
    return result.all()


async def user_create(
        session: AsyncSession,
        user_create: UserCreate,
) -> User:
    user = User(**user_create.model_dump())
    session.add(user)
    await session.commit()
    #await session.refresh(user)
    return user