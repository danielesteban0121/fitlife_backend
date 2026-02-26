from jose import jwt
from datetime import datetime, timedelta
import uuid

SECRET_KEY = "supersecret"
ALGORITHM = "HS256"

class JWTTokenManager:

    @staticmethod
    def create_access_token(subject: str) -> str:
        payload = {
            "sub": subject,
            "jti": str(uuid.uuid4()),
            "exp": datetime.utcnow() + timedelta(minutes=30)
        }
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def verify_token(token: str):
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])