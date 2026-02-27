from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from ..enums.user_role import UserRole
from ..value_objects.email import Email


@dataclass
class User:
    id: UUID
    email: Email
    password_hash: str
    role: UserRole
    is_active: bool
    created_at: datetime

    def deactivate(self):
        self.is_active = False
