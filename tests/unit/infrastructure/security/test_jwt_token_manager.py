from src.infrastructure.security.jwt_token_manager import JWTTokenManager


def test_create_and_verify_token():
    manager = JWTTokenManager(
        secret_key="this_is_a_super_secret_key_with_at_least_32_chars",
        access_token_expire_minutes=5,
    )

    token, expires_in = manager.create_access_token(
    user_id="123",
    role="USER",
    )

    payload = manager.verify_token(token)

    assert payload["sub"] == "123"
    assert payload["role"] == "USER"
    assert "jti" in payload
