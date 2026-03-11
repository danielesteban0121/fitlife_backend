from typing import List
from uuid import UUID
from src.domain.repositories.message_repository import MessageRepository
from src.application.dtos.message_dtos import MessageResponse


class GetMessages:
    def __init__(self, message_repository: MessageRepository):
        self.message_repository = message_repository

    async def execute(
        self, user_id: UUID, skip: int = 0, limit: int = 50
    ) -> List[MessageResponse]:
        messages = await self.message_repository.get_messages_for_user(
            user_id, skip=skip, limit=limit
        )

        return [
            MessageResponse(
                id=m.id,
                sender_id=m.sender_id,
                recipient_id=m.recipient_id,
                content=m.content,
                message_type=m.message_type,
                created_at=m.created_at,
                read_at=m.read_at,
            )
            for m in messages
        ]
