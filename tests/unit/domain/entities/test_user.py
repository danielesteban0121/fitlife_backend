from uuid import uuid4
from datetime import datetime, UTC
from src.domain.entities.user import User
from src.domain.value_objects.email import Email


def test_user_deactivate():
    user = User(
        id=uuid4(),
        email=Email("user@test.com"),
        password_hash="hash",
        role="USER",
        is_active=True,
        created_at=datetime.now(UTC),
    )

    user.deactivate()
    assert user.is_active is False
