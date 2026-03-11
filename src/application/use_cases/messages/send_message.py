import uuid
from src.domain.entities.message import Message, MessageType
from src.domain.repositories.message_repository import MessageRepository
from src.domain.repositories.user_repository import UserRepository
from src.domain.exceptions.base import DomainException
from src.application.dtos.message_dtos import SendMessageRequestDTO, SendMessageResponseDTO

class SendMessage:
    def __init__(
        self,
        message_repository: MessageRepository,
        user_repository: UserRepository
    ):
        self.message_repository = message_repository
        self.user_repository = user_repository

    async def execute(self, request: SendMessageRequestDTO) -> SendMessageResponseDTO:
        recipient = await self.user_repository.find_by_id(request.recipient_id)
        if not recipient:
            raise DomainException(f"Recipient {request.recipient_id} no encontrado")

        if request.sender_id:
            sender = await self.user_repository.find_by_id(request.sender_id)
            if not sender:
                raise DomainException(f"Sender {request.sender_id} no encontrado")

        msg = Message(
            id=uuid.uuid4(),
            sender_id=request.sender_id,
            recipient_id=request.recipient_id,
            content=request.content,
            message_type=MessageType.DIRECT if request.sender_id else MessageType.SYSTEM_NOTIFICATION
        )

        saved_msg = await self.message_repository.save(msg)

        return SendMessageResponseDTO(
            message_id=saved_msg.id,
            created_at=saved_msg.created_at,
            success=True
        )
