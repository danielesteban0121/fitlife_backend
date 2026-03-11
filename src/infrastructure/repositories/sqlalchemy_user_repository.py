from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.user import User
from src.domain.entities.user_profile import UserProfile
from src.domain.entities.audit_log import AuditLog
from src.domain.repositories.user_repository import UserRepository
from src.domain.value_objects.email import Email
from src.infrastructure.database.models.user_model import UserModel
from src.infrastructure.database.models.user_profile_model import UserProfileModel
from src.infrastructure.database.models.audit_log_model import AuditLogModel
from src.infrastructure.mappers.user_mapper import UserMapper
from src.infrastructure.mappers.user_profile_mapper import UserProfileMapper
from src.infrastructure.mappers.audit_log_mapper import AuditLogMapper


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
        result = await self.session.execute(select(UserModel).where(UserModel.id == str(user_id)))
        model = result.scalar_one_or_none()
        return UserMapper.to_domain(model) if model else None

    async def find_by_email(self, email: Email):
        result = await self.session.execute(select(UserModel).where(UserModel.email == str(email)))
        model = result.scalar_one_or_none()
        return UserMapper.to_domain(model) if model else None

    async def exists_by_email(self, email: Email) -> bool:
        user = await self.find_by_email(email)
        return user is not None

    async def get_profile(self, user_id: UUID) -> Optional[UserProfile]:
        result = await self.session.execute(
            select(UserProfileModel).where(UserProfileModel.user_id == str(user_id))
        )
        model = result.scalar_one_or_none()
        return UserProfileMapper.to_domain(model) if model else None

    async def update_profile(self, profile: UserProfile) -> UserProfile:
        model = UserProfileMapper.to_model(profile)
        # Use merge here to handle update or insert if needed, but since it's an update_profile
        # we assume it already exists or we want to ensure it's saved.
        # Actually, for standard update in SQLAlchemy async, merging or fetching and updating is common.
        # Since the plan says update_profile, let's assume existence check happens in Use Case or here.
        await self.session.merge(model)
        await self.session.commit()
        return UserProfileMapper.to_domain(model)

    async def save_audit_log(self, audit_log: AuditLog) -> None:
        model = AuditLogMapper.to_model(audit_log)
        self.session.add(model)
        await self.session.commit()

    async def get_audit_logs(self, user_id: UUID) -> list[AuditLog]:
        result = await self.session.execute(
            select(AuditLogModel)
            .where(AuditLogModel.user_id == str(user_id))
            .order_by(AuditLogModel.timestamp.desc())
        )
        models = result.scalars().all()
        return [AuditLogMapper.to_domain(m) for m in models]
