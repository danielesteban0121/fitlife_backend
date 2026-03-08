import uuid
from datetime import datetime, timedelta

import jwt

from src.config.settings import settings


class JWTTokenManager:

    def __init__(self, secret_key: str, algorithm: str):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def create_token(self, user_id: str):

        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

        payload = {
            "sub": user_id,
            "exp": expire,
            "jti": str(uuid.uuid4()),
        }

        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def verify_token(self, token: str):

        return jwt.decode(
            token,
            self.secret_key,
            algorithms=[self.algorithm],
        )