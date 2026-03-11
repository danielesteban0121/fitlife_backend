from datetime import datetime
from uuid import uuid4, UUID
from src.domain.entities.audit_log import AuditLog
from src.domain.repositories.user_repository import UserRepository


class AuditService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def record_action(self, user_id: UUID, action: str, details: str | None = None) -> None:
        audit_log = AuditLog(
            id=uuid4(),
            user_id=user_id,
            action=action,
            details=details,
            timestamp=datetime.utcnow()
        )
        await self.user_repository.save_audit_log(audit_log)

    async def get_user_audit_logs(self, user_id: UUID) -> list[AuditLog]:
        return await self.user_repository.get_audit_logs(user_id)
