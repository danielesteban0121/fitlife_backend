from uuid import UUID

from src.domain.entities.message import Message
from src.infrastructure.database.models.message_model import MessageModel

class MessageMapper:
    @staticmethod
    def to_domain(model: MessageModel) -> Message:
        return Message(
            id=UUID(model.id),
            sender_id=UUID(model.sender_id) if model.sender_id else None,
            recipient_id=UUID(model.recipient_id),
            content=model.content,
            message_type=model.message_type,
            created_at=model.created_at,
            read_at=model.read_at
        )

    @staticmethod
    def to_model(domain: Message) -> MessageModel:
        return MessageModel(
            id=str(domain.id),
            sender_id=str(domain.sender_id) if domain.sender_id else None,
            recipient_id=str(domain.recipient_id),
            content=domain.content,
            message_type=domain.message_type,
            created_at=domain.created_at,
            read_at=domain.read_at
        )
