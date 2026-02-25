from datetime import datetime, timedelta
from jose import jwt
import uuid

from src.config.settings import settings


class JWTTokenManager:

    def create_token(self, user_id: str):
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

        payload = {"sub": user_id, "exp": expire, "jti": str(uuid.uuid4())}

        return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    def verify_token(self, token: str):
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
