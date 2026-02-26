import pytest
from uuid import uuid4
from datetime import datetime, UTC
from src.domain.entities.user import User
from src.domain.value_objects.email import Email
from src.domain.enums.user_role import UserRole
from src.infrastructure.repositories.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository,
)


@pytest.mark.asyncio
async def test_user_repository_save_and_find(session):
    repo = SQLAlchemyUserRepository(session)

    user = User(
        id=uuid4(),
        email=Email("integration@test.com"),
        password_hash="hash",
        role=UserRole.USER,
        is_active=True,
        created_at=datetime.now(UTC),
    )

    await repo.save(user)

    found = await repo.find_by_email(Email("integration@test.com"))

    assert found is not None
    assert found.email.value == "integration@test.com"
