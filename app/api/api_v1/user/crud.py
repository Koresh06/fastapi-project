from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result
from .schemas import UserCreateWithHashedPassword

from core.models import User


# async def get_all_users(session: AsyncSession) -> Sequence[User]:
#     stmt = select(User).order_by(User.id)
#     result: Result = await session.scalars(stmt)
#     return result.all()
