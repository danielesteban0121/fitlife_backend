from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4
from datetime import datetime, UTC

import pytest

from src.application.use_cases.auth.change_password import ChangePassword
from src.application.dtos.auth_dtos import ChangePasswordRequest
from src.domain.entities.user import User
from src.domain.enums.user_role import UserRole
from src.domain.value_objects.email import Email
from src.domain.exceptions.user_exceptions import InvalidCredentials
from src.domain.exceptions.validation_exceptions import InvalidValueException


@pytest.mark.asyncio
async def test_change_password_success():
    # Arrange
    repository = MagicMock()
    repository.find_by_id = AsyncMock()
    repository.save = AsyncMock()
    
    hasher = MagicMock()
    hasher.verify.return_value = True
    hasher.hash.return_value = "new_hashed_password"
    
    use_case = ChangePassword(repository, hasher)
    
    user_id = uuid4()
    user = User(
        id=user_id,
        email=Email("test@example.com"),
        password_hash="old_hashed_password",
        role=UserRole.USER,
        is_active=True,
        created_at=datetime.now(UTC)
    )
    repository.find_by_id.return_value = user
    
    request = ChangePasswordRequest(
        current_password="OldPassword123!",
        new_password="NewPassword456!"
    )

    # Act
    result = await use_case.execute(user_id, request)

    # Assert
    assert result.message == "Contraseña actualizada correctamente"
    assert user.password_hash == "new_hashed_password"
    repository.save.assert_called_once_with(user)


@pytest.mark.asyncio
async def test_change_password_invalid_current():
    # Arrange
    repository = MagicMock()
    repository.find_by_id = AsyncMock()
    
    hasher = MagicMock()
    hasher.verify.return_value = False
    
    use_case = ChangePassword(repository, hasher)
    
    user_id = uuid4()
    user = User(
        id=user_id,
        email=Email("test@example.com"),
        password_hash="old_hashed_password",
        role=UserRole.USER,
        is_active=True,
        created_at=datetime.now(UTC)
    )
    repository.find_by_id.return_value = user
    
    request = ChangePasswordRequest(
        current_password="WrongPassword",
        new_password="NewPassword456!"
    )

    # Act & Assert
    with pytest.raises(InvalidCredentials):
        await use_case.execute(user_id, request)


@pytest.mark.asyncio
async def test_change_password_policy_violation():
    # Arrange
    repository = MagicMock()
    repository.find_by_id = AsyncMock()
    
    hasher = MagicMock()
    hasher.verify.return_value = True
    
    use_case = ChangePassword(repository, hasher)
    
    user_id = uuid4()
    user = User(
        id=user_id,
        email=Email("test@example.com"),
        password_hash="old_hashed_password",
        role=UserRole.USER,
        is_active=True,
        created_at=datetime.now(UTC)
    )
    repository.find_by_id.return_value = user
    
    # New password passes DTO (min_length=8) but fails PasswordValidator (no digit)
    request = ChangePasswordRequest(
        current_password="OldPassword123!",
        new_password="PasswordNoDigit"
    )


    # Act & Assert
    with pytest.raises(InvalidValueException):
        await use_case.execute(user_id, request)
