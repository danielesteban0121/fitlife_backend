
from uuid import UUID

from src.domain.entities.user_profile import UserProfile
from src.infrastructure.database.models.user_profile_model import UserProfileModel


class UserProfileMapper:
    @staticmethod
    def to_domain(model: UserProfileModel) -> UserProfile:
        return UserProfile(
            id=UUID(model.id),
            user_id=UUID(model.user_id),
            full_name=model.full_name,
            date_of_birth=model.date_of_birth,
            height_cm=model.height_cm,
        )

    @staticmethod
    def to_model(entity: UserProfile) -> UserProfileModel:
        return UserProfileModel(
            id=str(entity.id),
            user_id=str(entity.user_id),
            full_name=entity.full_name,
            date_of_birth=entity.date_of_birth,
            height_cm=entity.height_cm,
        )
