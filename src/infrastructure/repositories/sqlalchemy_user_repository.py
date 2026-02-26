from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from src.domain.repositories.user_repository import UserRepository
from src.domain.entities.user import User
from src.domain.value_objects.email import Email
from src.infrastructure.database.models.user_model import UserModel
from src.infrastructure.mappers.user_mapper import UserMapper

class SQLAlchemyUserRepository(UserRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, user: User) -> User:
        model = UserMapper.to_model(user)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return UserMapper.to_domain(model)

    async def find_by_id(self, user_id: UUID):
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == str(user_id))
        )
        model = result.scalar_one_or_none()
        return UserMapper.to_domain(model) if model else None

    async def find_by_email(self, email: Email):
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == str(email))
        )
        model = result.scalar_one_or_none()
        return UserMapper.to_domain(model) if model else None

    async def exists_by_email(self, email: Email) -> bool:
        user = await self.find_by_email(email)
        return user is not None