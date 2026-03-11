from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

class MessageType(str, Enum):
    DIRECT = "DIRECT"
    SYSTEM_NOTIFICATION = "SYSTEM_NOTIFICATION"

@dataclass
class Message:
    """Entidad de dominio para Mensajes y Notificaciones."""
    id: UUID
    sender_id: Optional[UUID] # None para notificaciones del sistema
    recipient_id: UUID
    content: str
    message_type: MessageType = MessageType.DIRECT
    created_at: datetime = field(default_factory=datetime.utcnow)
    read_at: Optional[datetime] = None

    def mark_as_read(self, read_at: Optional[datetime] = None):
        self.read_at = read_at or datetime.utcnow()
