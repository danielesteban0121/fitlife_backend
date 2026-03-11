from typing import List
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.message import Message
from src.domain.repositories.message_repository import MessageRepository
from src.infrastructure.database.models.message_model import MessageModel
from src.infrastructure.mappers.message_mapper import MessageMapper

class SQLAlchemyMessageRepository(MessageRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, message: Message) -> Message:
        model = MessageMapper.to_model(message)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return MessageMapper.to_domain(model)

    async def get_messages_for_user(self, user_id: UUID, skip: int = 0, limit: int = 50) -> List[Message]:
        result = await self.session.execute(
            select(MessageModel)
            .where(MessageModel.recipient_id == str(user_id))
            .order_by(MessageModel.created_at.desc())
            .offset(skip).limit(limit)
        )
        models = result.scalars().all()
        return [MessageMapper.to_domain(m) for m in models]

    async def get_unread_count(self, user_id: UUID) -> int:
        result = await self.session.execute(
            select(func.count(MessageModel.id))
            .where(MessageModel.recipient_id == str(user_id))
            .where(MessageModel.read_at == None)
        )
        return result.scalar_one() or 0
