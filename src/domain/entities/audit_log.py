from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class AuditLog:
    id: UUID
    user_id: UUID
    action: str
    details: str | None
    timestamp: datetime
