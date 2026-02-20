from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from ..value_objects.email import Email
from ..enums.user_role import UserRole

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