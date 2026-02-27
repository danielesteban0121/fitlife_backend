import pytest
from unittest.mock import AsyncMock, Mock

from src.application.use_cases.auth.register_user import RegisterUser
from src.application.dtos.auth_dtos import RegisterUserRequest
from src.domain.entities.user import User
from src.domain.enums.user_role import UserRole
from src.domain.value_objects.email import Email


@pytest.mark.asyncio
async def test_register_user_success():
    mock_repo = AsyncMock()
    mock_hasher = Mock()
    mock_jwt = Mock()

    mock_repo.find_by_email.return_value = None
    mock_hasher.hash.return_value = "hashed_password"
    mock_jwt.create_access_token.return_value = ("token", 1800)

    use_case = RegisterUser(
        user_repository=mock_repo,
        password_hasher=mock_hasher,
        jwt_manager=mock_jwt,
    )

    request = RegisterUserRequest(
        email="test@example.com",
        password="Password123!",
    )

    mock_repo.save.return_value = User(
        id="123",
        email=Email("test@example.com"),
        password_hash="hashed_password",
        role=UserRole.USER,
        is_active=True,
        created_at=None,
    )

    response = await use_case.execute(request)

    assert response.email == "test@example.com"
    assert response.access_token == "token"
    assert response.expires_in == 1800
