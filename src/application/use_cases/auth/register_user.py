from uuid import uuid4
from datetime import datetime, UTC

from src.domain.entities.user import User
from src.domain.enums.user_role import UserRole
from src.domain.value_objects.email import Email
from src.domain.repositories.user_repository import UserRepository
from src.domain.exceptions.user_exceptions import EmailAlreadyExistsException

from src.application.dtos.auth_dtos import (
    RegisterUserRequest,
    RegisterUserResponse,
)


class RegisterUser:
    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher,
        jwt_manager,
    ):
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        self.jwt_manager = jwt_manager

    async def execute(
        self,
        request: RegisterUserRequest,
    ) -> RegisterUserResponse:
        email = Email(request.email)

        existing_user = await self.user_repository.find_by_email(email)
        if existing_user:
            raise EmailAlreadyExistsException(f"Email {request.email} ya registrado")

        password_hash = self.password_hasher.hash(request.password)

        user = User(
            id=str(uuid4()),
            email=email,
            password_hash=password_hash,
            role=UserRole.USER,
            is_active=True,
            created_at=datetime.now(UTC),
        )

        saved_user = await self.user_repository.save(user)

        access_token, expires_in = self.jwt_manager.create_access_token(
    user_id=str(user.id),
    role=user.role,
)

        return RegisterUserResponse(
            user_id=str(saved_user.id),
            email=str(saved_user.email),
            access_token=access_token,
            expires_in=expires_in,
        )
