from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.physical_record import PhysicalRecord
from src.domain.repositories.physical_record_repository import PhysicalRecordRepository
from src.infrastructure.database.models.physical_record_model import PhysicalRecordModel
from src.infrastructure.mappers.physical_record_mapper import PhysicalRecordMapper


class SQLAlchemyPhysicalRecordRepository(PhysicalRecordRepository):
    """Implementación SQLAlchemy del repositorio de registros físicos."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, record: PhysicalRecord) -> PhysicalRecord:
        model = PhysicalRecordMapper.to_model(record)
        # Usamos merge por si el ID ya existe y queremos actualizar
        await self.session.merge(model)
        await self.session.commit()
        return record

    async def find_by_user_id(self, user_id: UUID) -> List[PhysicalRecord]:
        stmt = (
            select(PhysicalRecordModel)
            .where(PhysicalRecordModel.user_id == str(user_id))
            .order_by(PhysicalRecordModel.recorded_at.desc())
        )
        result = await self.session.execute(stmt)
        models = result.scalars().all()
        return [PhysicalRecordMapper.to_domain(m) for m in models]

    async def find_latest_by_user_id(self, user_id: UUID) -> Optional[PhysicalRecord]:
        stmt = (
            select(PhysicalRecordModel)
            .where(PhysicalRecordModel.user_id == str(user_id))
            .order_by(PhysicalRecordModel.recorded_at.desc())
            .limit(1)
        )
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return PhysicalRecordMapper.to_domain(model) if model else None

    async def find_by_id(self, record_id: UUID) -> Optional[PhysicalRecord]:
        stmt = select(PhysicalRecordModel).where(PhysicalRecordModel.id == str(record_id))
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return PhysicalRecordMapper.to_domain(model) if model else None

    async def delete(self, record_id: UUID) -> None:
        stmt = select(PhysicalRecordModel).where(PhysicalRecordModel.id == str(record_id))
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model:
            await self.session.delete(model)
            await self.session.commit()
