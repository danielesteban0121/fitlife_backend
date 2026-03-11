from uuid import UUID
from src.domain.entities.audit_log import AuditLog
from src.infrastructure.database.models.audit_log_model import AuditLogModel

class AuditLogMapper:
    @staticmethod
    def to_domain(model: AuditLogModel) -> AuditLog:
        return AuditLog(
            id=UUID(model.id),
            user_id=UUID(model.user_id),
            action=model.action,
            details=model.details,
            timestamp=model.timestamp
        )

    @staticmethod
    def to_model(entity: AuditLog) -> AuditLogModel:
        return AuditLogModel(
            id=str(entity.id),
            user_id=str(entity.user_id),
            action=entity.action,
            details=entity.details,
            timestamp=entity.timestamp
        )
