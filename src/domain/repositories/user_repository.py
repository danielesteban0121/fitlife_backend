from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from ..entities.user import User
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
