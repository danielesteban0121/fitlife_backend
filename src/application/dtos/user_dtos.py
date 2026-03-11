from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


class UserProfileResponse(BaseModel):
    user_id: str
    email: str
    full_name: str
    date_of_birth: Optional[date] = None
    height_cm: Optional[float] = None
    role: str
    created_at: datetime


class UpdateUserProfileRequest(BaseModel):
    full_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    height_cm: Optional[float] = Field(None, ge=50, le=300)


class AuditLogResponse(BaseModel):
    id: str
    user_id: str
    action: str
    details: Optional[str] = None
    timestamp: datetime
