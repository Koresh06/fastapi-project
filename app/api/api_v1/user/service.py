import uuid
from sqlalchemy import desc, select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.user import User
from core.models.blacklisted_tokens import BlacklistedToken
from api.api_v1.auth.schemas import UserCreateModel
from api.api_v1.user.schemas import UserUpdateModel
from api.api_v1.auth.utils import generate_passwd_hash


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def delete_user(self, user: User):
        await self.session.delete(user)
        await self.session.commit()


    async def update_user(
            self, 
            user: User,
            user_update: UserUpdateModel,
            partil: bool = False
            ) -> User:
        for field, value in user_update.model_dump(exclude_unset=partil).items():
            setattr(user, field, value)
        await self.session.commit()
        return user


    async def get_user_uid(self, uid: uuid.UUID) -> User | None:
        stmt: Result = await self.session.scalar(select(User).where(User.uid == uid))
        return stmt

    async def get_user_username(self, username: str) -> User | None:
        stmt: Result = await self.session.scalar(select(User).where(User.username == username))
        return stmt if stmt else None


    async def get_all_users(self, limit: int, offset: int) -> list[User] | None:
        statement = select(User).order_by(desc(User.created_at)).limit(limit).offset(offset)
        stmt: Result = await self.session.scalars(statement)
        return stmt


    async def create_user(self, user_details: UserCreateModel):
        user_dict = user_details.model_dump()
        hashed_password = generate_passwd_hash(user_dict["hashed_password"])
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