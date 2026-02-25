from datetime import UTC, datetime
from uuid import uuid4

import pytest

from src.domain.entities.user import User
from src.domain.enums.user_role import UserRole
from src.domain.value_objects.email import Email


@pytest.mark.asyncio
async def test_create_user(user_repo):
    user = User(
        id=str(uuid4()),
        email=Email(f"{uuid4()}@test.com"),
        password_hash="123456",
        role=UserRole.USER,
        is_active=True,
        created_at=datetime.now(UTC),
    )

    saved_user = await user_repo.save(user)

    assert saved_user is not None
    assert saved_user.email.value.endswith("@test.com")


@pytest.mark.asyncio
async def test_get_user_by_email(user_repo):
    email = Email(f"{uuid4()}@test.com")

    user = User(
        id=str(uuid4()),
        email=email,
        password_hash="123456",
        role=UserRole.USER,
        is_active=True,
        created_at=datetime.now(UTC),
    )

    await user_repo.save(user)

    found_user = await user_repo.find_by_email(email)

    assert found_user is not None
    assert found_user.email.value == email.value


@pytest.mark.asyncio
async def test_user_not_found(user_repo):
    email = Email(f"{uuid4()}@test.com")

    result = await user_repo.find_by_email(email)

    assert result is None
