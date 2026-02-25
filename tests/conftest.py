import pytest_asyncio

from src.domain.entities.user import User
from src.domain.value_objects.email import Email


@pytest_asyncio.fixture
async def user_repo():
    """
    Fake repository para pruebas unitarias (no usa base de datos real)
    """

    class FakeUserRepository:
        def __init__(self):
            self.users = []

        async def save(self, user: User):
            self.users.append(user)
            return user

        async def find_by_email(self, email: Email):
            for user in self.users:
                if user.email.value == email.value:
                    return user
            return None

    return FakeUserRepository()
