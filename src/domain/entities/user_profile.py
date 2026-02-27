from dataclasses import dataclass
from datetime import date
from uuid import UUID



@dataclass
class UserProfile:
    id: UUID
    user_id: UUID
    full_name: str
    date_of_birth: date | None
    height_cm: float | None
