from src.infrastructure.security.jwt_token_manager import JWTTokenManager

def test_create_and_verify_token():
    token = JWTTokenManager.create_access_token("user_id")
    payload = JWTTokenManager.verify_token(token)
    assert payload["sub"] == "user_id"