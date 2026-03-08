from unittest.mock import Mock

import pytest

from src.application.use_cases.auth.refresh_token import RefreshToken


@pytest.mark.asyncio
async def test_refresh_token_success():
    mock_jwt = Mock()

    # El token válido trae type: "refresh"
    mock_jwt.verify_token.return_value = {"sub": "user-123", "role": "USER", "type": "refresh"}

    # Mokear generación de los nuevos tokens
    mock_jwt.create_access_token.return_value = ("new_access_token", 1800)
    mock_jwt.create_refresh_token.return_value = "new_refresh_token"

    use_case = RefreshToken(token_manager=mock_jwt)

    response = await use_case.execute("valid_refresh_token")

    assert response["access_token"] == "new_access_token"
    assert response["refresh_token"] == "new_refresh_token"
    assert response["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_refresh_token_invalid_type_raises_error():
    mock_jwt = Mock()

    # Pasa un token de acceso al endpoint de refresh
    mock_jwt.verify_token.return_value = {"sub": "user-123", "role": "USER", "type": "access"}

    use_case = RefreshToken(token_manager=mock_jwt)

    with pytest.raises(ValueError, match="Invalid token type"):
        await use_case.execute("valid_access_token")
