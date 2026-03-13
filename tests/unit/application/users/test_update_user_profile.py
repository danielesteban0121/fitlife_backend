from unittest.mock import ANY, AsyncMock, MagicMock
from uuid import uuid4
from datetime import date, datetime, UTC

import pytest

from src.application.use_cases.users.update_user_profile import UpdateUserProfile
from src.application.dtos.user_dtos import UpdateUserProfileRequest
from src.domain.entities.user import User
from src.domain.entities.user_profile import UserProfile
from src.domain.enums.user_role import UserRole
from src.domain.value_objects.email import Email


@pytest.mark.asyncio
async def test_update_user_profile_success():
    # Arrange
    user_repository = MagicMock()
    user_repository.find_by_id = AsyncMock()
    user_repository.get_profile = AsyncMock()
    user_repository.update_profile = AsyncMock()
    
    audit_service = MagicMock()
    audit_service.record_action = AsyncMock()
    
    use_case = UpdateUserProfile(user_repository, audit_service)
    
    user_id = uuid4()
    user = User(
        id=user_id,
        email=Email("test@example.com"),
        password_hash="hash",
        role=UserRole.USER,
        is_active=True,
        created_at=datetime.now(UTC)
    )
    user_repository.find_by_id.return_value = user
    
    existing_profile = UserProfile(
        id=uuid4(),
        user_id=user_id,
        full_name="Old Name",
        date_of_birth=date(1990, 1, 1),
        height_cm=170.0
    )
    user_repository.get_profile.return_value = existing_profile
    user_repository.update_profile.side_effect = lambda p: p
    
    request = UpdateUserProfileRequest(
        full_name="New Name",
        height_cm=175.0
    )

    # Act
    result = await use_case.execute(user_id, request)

    # Assert
    assert result.full_name == "New Name"
    assert result.height_cm == 175.0
    assert result.date_of_birth == date(1990, 1, 1) # Unchanged
    user_repository.update_profile.assert_called_once()
    audit_service.record_action.assert_called_once_with(
        user_id, "UPDATE_PROFILE", ANY
    )
