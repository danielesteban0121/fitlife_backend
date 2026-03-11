from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from ..entities.user import User
from ..entities.user_profile import UserProfile
from ..entities.audit_log import AuditLog
from ..value_objects.email import Email


class UserRepository(ABC):

    @abstractmethod
    async def save(self, user: User) -> User:
        pass

    @abstractmethod
    async def find_by_id(self, user_id: UUID) -> Optional[User]:
        pass

    @abstractmethod
    async def find_by_email(self, email: Email) -> Optional[User]:
        pass

    @abstractmethod
    async def exists_by_email(self, email: Email) -> bool:
        pass

    @abstractmethod
    async def get_profile(self, user_id: UUID) -> Optional[UserProfile]:
        pass

    @abstractmethod
    async def update_profile(self, profile: UserProfile) -> UserProfile:
        pass

    @abstractmethod
    async def save_audit_log(self, audit_log: AuditLog) -> None:
        pass

    @abstractmethod
    async def get_audit_logs(self, user_id: UUID) -> list[AuditLog]:
        pass
