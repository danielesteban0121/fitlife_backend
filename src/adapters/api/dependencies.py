from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
import jwt

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

from src.config.settings import settings


from src.application.use_cases.auth.register_user import RegisterUser
from src.application.use_cases.auth.login_user import LoginUser
from src.application.use_cases.auth.refresh_token import RefreshToken


def get_register_user(
    db: AsyncSession = Depends(get_db),
) -> RegisterUser:

    repo = SQLAlchemyUserRepository(db)
    hasher = BCryptPasswordHasher()

    token_manager = JWTTokenManager(
        settings.SECRET_KEY,
        settings.ALGORITHM,
    )

    return RegisterUser(repo, hasher, token_manager)


def get_login_user(
    db: AsyncSession = Depends(get_db),
) -> LoginUser:

    repo = SQLAlchemyUserRepository(db)
    hasher = BCryptPasswordHasher()

    token_manager = JWTTokenManager(
        settings.SECRET_KEY,
        settings.ALGORITHM,
    )

    return LoginUser(repo, hasher, token_manager)


def get_refresh_token() -> RefreshToken:

    token_manager = JWTTokenManager(
        settings.SECRET_KEY,
        settings.ALGORITHM,
    )

    return RefreshToken(token_manager)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        token_manager = JWTTokenManager(
            settings.SECRET_KEY,
            settings.ALGORITHM,
        )
        payload = token_manager.verify_token(token)

        if payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return {
            "user_id": payload.get("sub"),
            "role": payload.get("role"),
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


from src.infrastructure.repositories.sqlalchemy_assessment_repository import (
    SQLAlchemyAssessmentRepository,
)
from src.domain.services.assessment_calculator import AssessmentCalculator
from src.application.use_cases.assessments.submit_assessment import SubmitAssessment


def get_submit_assessment(
    db: AsyncSession = Depends(get_db),
) -> SubmitAssessment:
    repo = SQLAlchemyAssessmentRepository(db)
    calc = AssessmentCalculator()
    return SubmitAssessment(repo, calc)
