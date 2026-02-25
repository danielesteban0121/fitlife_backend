from dataclasses import dataclass
from uuid import UUID
from datetime import date


@dataclass
class UserProfile:
    id: UUID
    user_id: UUID
    full_name: str
    date_of_birth: date | None
    height_cm: float | None
