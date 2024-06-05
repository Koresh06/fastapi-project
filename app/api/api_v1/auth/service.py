from passlib.context import CryptContext
from sqlalchemy import desc, select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.user import User
from core.models.blacklisted_tokens import BlacklistedToken
from .schemas import UserCreationModel
from .utils import create_password_hash
from core.config import settings


SECRET_KEY = settings.auth.secret_key
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user(self, username: str) -> User | None:
        """get single user"""
        stmt = await self.session.scalar(select(User).where(User.username == username))

        return stmt if stmt else None

    async def get_all_users(self) -> list[User]:
        """get all users"""
        statement = select(User).order_by(desc(User.created_at))

        stmt: Result = await self.session.scalars(statement)

        return stmt

    async def create_user(self, user_details: UserCreationModel):
        """create user"""
        user_dict = user_details.model_dump()

        hashed_password = create_password_hash(user_dict["hashed_password"])

        user_dict["hashed_password"] = hashed_password

        new_user = User(**user_dict)

        self.session.add(new_user)
        await self.session.commit()

        return new_user
    

    async def add_token_to_blacklist(self, token: str, session: AsyncSession):
        try:

            self.session.add(BlacklistedToken(token=token))
            await session.commit()
            return True
        except Exception as e:
            return False