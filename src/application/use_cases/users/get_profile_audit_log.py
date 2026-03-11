from uuid import UUID
from src.application.dtos.user_dtos import AuditLogResponse
from src.application.services.audit_service import AuditService


class GetProfileAuditLog:
    def __init__(self, audit_service: AuditService):
        self.audit_service = audit_service

    async def execute(self, user_id: UUID) -> list[AuditLogResponse]:
        logs = await self.audit_service.get_user_audit_logs(user_id)
        
        return [
            AuditLogResponse(
                id=str(log.id),
                user_id=str(log.user_id),
                action=log.action,
                details=log.details,
                timestamp=log.timestamp
            )
            for log in logs
        ]
