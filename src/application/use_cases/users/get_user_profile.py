from uuid import UUID
from src.application.dtos.user_dtos import UserProfileResponse
from src.domain.repositories.user_repository import UserRepository
from src.application.services.audit_service import AuditService


class GetUserProfile:
    def __init__(self, user_repository: UserRepository, audit_service: AuditService):
        self.user_repository = user_repository
        self.audit_service = audit_service

    async def execute(self, user_id: UUID) -> UserProfileResponse:
        user = await self.user_repository.find_by_id(user_id)
        if not user:
            raise Exception("Usuario no encontrado")

        profile = await self.user_repository.get_profile(user_id)
        
        # Record access in audit log
        await self.audit_service.record_action(user_id, "VIEW_PROFILE", "User viewed their own profile")

        return UserProfileResponse(
            user_id=str(user.id),
            email=str(user.email),
            full_name=profile.full_name if profile else "No asignado",
            date_of_birth=profile.date_of_birth if profile else None,
            height_cm=profile.height_cm if profile else None,
            role=user.role.value if hasattr(user.role, "value") else str(user.role),
            created_at=user.created_at
        )
