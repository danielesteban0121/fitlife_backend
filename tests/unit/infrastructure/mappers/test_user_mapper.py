from datetime import UTC, datetime
from uuid import uuid4

from src.domain.entities.user import User
from src.domain.enums.user_role import UserRole
from src.domain.value_objects.email import Email
from src.infrastructure.mappers.user_mapper import UserMapper


def test_user_mapper_roundtrip():
    user = User(
        id=uuid4(),
        email=Email("test@test.com"),
        password_hash="hash",
        role=UserRole.USER,
        is_active=True,
        created_at=datetime.now(UTC),
    )

    model = UserMapper.to_model(user)
    domain_back = UserMapper.to_domain(model)

    assert domain_back.email.value == "test@test.com"
