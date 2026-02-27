from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.connection import get_db
from src.infrastructure.repositories.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository,
)
from src.infrastructure.security.bcrypt_password_hasher import (
    BCryptPasswordHasher,
)
from src.infrastructure.security.jwt_token_manager import (
    JWTTokenManager,
)
from src.application.use_cases.auth.register_user import RegisterUser
from src.config.settings import settings


def get_register_user_use_case(
    session: AsyncSession = Depends(get_db),
) -> RegisterUser:
    repo = SQLAlchemyUserRepository(session)
    hasher = BCryptPasswordHasher()

    jwt_manager = JWTTokenManager(
    secret_key=settings.jwt_secret_key,
    algorithm=settings.jwt_algorithm,
    access_token_expire_minutes=settings.jwt_expiration_minutes,
)
    return RegisterUser(repo, hasher, jwt_manager)