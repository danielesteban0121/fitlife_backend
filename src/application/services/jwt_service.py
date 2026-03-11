from src.infrastructure.security.jwt_token_manager import JWTTokenManager


class JWTService:
    def __init__(self, token_manager: JWTTokenManager):
        self.token_manager = token_manager

    def create_access_token(self, user_id: str, role: str) -> tuple[str, int]:
        return self.token_manager.create_access_token(user_id, role)

    def create_refresh_token(self, user_id: str, role: str) -> str:
        return self.token_manager.create_refresh_token(user_id, role)

    def verify_token(self, token: str) -> dict:
        return self.token_manager.verify_token(token)
