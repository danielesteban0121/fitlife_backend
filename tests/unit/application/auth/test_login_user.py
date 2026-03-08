import pytest
from unittest.mock import AsyncMock, Mock

from src.application.use_cases.auth.login_user import LoginUser
from src.domain.entities.user import User
from src.domain.enums.user_role import UserRole
from src.domain.value_objects.email import Email


@pytest.mark.asyncio
async def test_login_user_success():
    mock_repo = AsyncMock()
    mock_hasher = Mock()
    mock_jwt = Mock()

    # Usuario mokeado devuelto por el repositorio
    mock_user = User(
        id="123",
        email=Email("test@example.com"),
        password_hash="hashed_password",
        role=UserRole.USER,
        is_active=True,
        created_at=None,
    )

    mock_repo.find_by_email.return_value = mock_user
    mock_hasher.verify.return_value = True
    mock_jwt.create_access_token.return_value = ("access_token_123", 1800)
    mock_jwt.create_refresh_token.return_value = "refresh_token_123"

    use_case = LoginUser(
        user_repository=mock_repo,
        password_hasher=mock_hasher,
        jwt_manager=mock_jwt,
    )

    response = await use_case.execute("test@example.com", "Password123!")

    assert response["access_token"] == "access_token_123"
    assert response["refresh_token"] == "refresh_token_123"
    assert response["expires_in"] == 1800


@pytest.mark.asyncio
async def test_login_user_invalid_credentials_returns_error():
    mock_repo = AsyncMock()
    mock_hasher = Mock()
    mock_jwt = Mock()

    # Usuario no encontrado
    mock_repo.find_by_email.return_value = None

    use_case = LoginUser(
        user_repository=mock_repo,
        password_hasher=mock_hasher,
        jwt_manager=mock_jwt,
    )

    with pytest.raises(ValueError, match="Invalid credentials"):
        await use_case.execute("wrong@example.com", "Password123!")
