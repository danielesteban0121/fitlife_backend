from src.infrastructure.security.jwt_token_manager import JWTTokenManager


class RefreshToken:

    def __init__(self, token_manager: JWTTokenManager):
        self.token_manager = token_manager

    async def execute(self, token: str):

        payload = self.token_manager.verify_token(token)

        if payload.get("type") != "refresh":
            raise ValueError("Invalid token type")

        user_id = payload["sub"]
        role = payload.get("role")

        new_access_token, _ = self.token_manager.create_access_token(user_id, role)
        new_refresh_token = self.token_manager.create_refresh_token(user_id, role)

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
        }
