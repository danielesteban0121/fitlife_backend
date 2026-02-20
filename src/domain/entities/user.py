from dataclasses import dataclass, field
from datetime import datetime, UTC
from uuid import UUID
from ..value_objects.email import Email


@dataclass
class User:
    id: UUID
    email: Email
    password_hash: str
    role: str
    is_active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def deactivate(self):
        self.is_active = False
