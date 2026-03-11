from uuid import UUID, uuid4
from src.application.dtos.user_dtos import UpdateUserProfileRequest, UserProfileResponse
from src.domain.entities.user_profile import UserProfile
from src.domain.repositories.user_repository import UserRepository
from src.application.services.audit_service import AuditService


class UpdateUserProfile:
    def __init__(self, user_repository: UserRepository, audit_service: AuditService):
        self.user_repository = user_repository
        self.audit_service = audit_service

    async def execute(self, user_id: UUID, request: UpdateUserProfileRequest) -> UserProfileResponse:
        user = await self.user_repository.find_by_id(user_id)
        if not user:
            raise Exception("Usuario no encontrado")

        profile = await self.user_repository.get_profile(user_id)
        
        if not profile:
            profile = UserProfile(
                id=uuid4(),
                user_id=user_id,
                full_name=request.full_name or "Usuario",
                date_of_birth=request.date_of_birth,
                height_cm=request.height_cm
            )
        else:
            if request.full_name:
                profile.full_name = request.full_name
            if request.date_of_birth:
                profile.date_of_birth = request.date_of_birth
            if request.height_cm:
                profile.height_cm = request.height_cm

        updated_profile = await self.user_repository.update_profile(profile)
        
        # Record update in audit log
        await self.audit_service.record_action(user_id, "UPDATE_PROFILE", f"Updated profile fields: {request.model_dump_json(exclude_none=True)}")

        return UserProfileResponse(
            user_id=str(user.id),
            email=str(user.email),
            full_name=updated_profile.full_name,
            date_of_birth=updated_profile.date_of_birth,
            height_cm=updated_profile.height_cm,
            role=user.role.value if hasattr(user.role, "value") else str(user.role),
            created_at=user.created_at
        )
