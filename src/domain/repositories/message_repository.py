from abc import ABC, abstractmethod
from typing import List
from uuid import UUID
from ..entities.message import Message

class MessageRepository(ABC):
    """Puerto de salida para persistencia de mensajes y notificaciones."""
    
    @abstractmethod
    async def save(self, message: Message) -> Message:
        pass
        
    @abstractmethod
    async def get_messages_for_user(self, user_id: UUID, skip: int = 0, limit: int = 50) -> List[Message]:
        pass

    @abstractmethod
    async def get_unread_count(self, user_id: UUID) -> int:
        pass
