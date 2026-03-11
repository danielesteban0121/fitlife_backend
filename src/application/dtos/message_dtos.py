from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID
from src.domain.entities.message import MessageType


class MessageResponse(BaseModel):
    id: UUID
    sender_id: Optional[UUID]
    recipient_id: UUID
    content: str
    message_type: MessageType
    created_at: datetime
    read_at: Optional[datetime]


class SendMessageRequest(BaseModel):
    sender_id: Optional[UUID]
    recipient_id: UUID
    content: str


class SendMessageResponse(BaseModel):
    message_id: UUID
    created_at: datetime
    success: bool
