import jwt
from datetime import datetime, timedelta, UTC
from uuid import uuid4


class JWTTokenManager:

    def __init__(
        self,
        secret_key: str,
        algorithm: str = "HS256",
        access_token_expire_minutes: int = 15,
        refresh_token_expire_days: int = 7,
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes
        self.refresh_token_expire_days = refresh_token_expire_days

    def create_access_token(self, user_id: str, role) -> tuple[str, int]:
        now = datetime.now(UTC)
        expire = now + timedelta(minutes=self.access_token_expire_minutes)

        payload = {
            "sub": user_id,
            # 🔥 Convertimos Enum a string
            "role": role.value if hasattr(role, "value") else role,
            "jti": str(uuid4()),
            "type": "access",
            "iat": now,
            "exp": expire,
        }

        token = jwt.encode(
            payload,
            self.secret_key,
            algorithm=self.algorithm,
        )

        expires_in = self.access_token_expire_minutes * 60

        return token, expires_in

    def create_refresh_token(self, user_id: str, role) -> str:
        now = datetime.now(UTC)
        expire = now + timedelta(days=self.refresh_token_expire_days)

        payload = {
            "sub": user_id,
            "role": role.value if hasattr(role, "value") else role,
            "jti": str(uuid4()),
            "type": "refresh",
            "iat": now,
            "exp": expire,
        }

        token = jwt.encode(
            payload,
            self.secret_key,
            algorithm=self.algorithm,
        )

        return token

    def verify_token(self, token: str) -> dict:
        return jwt.decode(
            token,
            self.secret_key,
            algorithms=[self.algorithm],
        )
