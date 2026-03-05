import pytest_asyncio
from httpx import AsyncClient

from src.main import app

from src.domain.entities.user import User
from src.domain.value_objects.email import Email

from src.infrastructure.database.base import Base
from src.infrastructure.database.connection import engine


# ==============================
# DATABASE SETUP FOR TESTS
# ==============================

@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database():
    """
    Crea las tablas antes de los tests
    y las elimina al finalizar
    """

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# ==============================
# API CLIENT FIXTURE
# ==============================

@pytest_asyncio.fixture
async def client():
    """
    Cliente HTTP para tests de integración
    """

    async with AsyncClient(
        app=app,
        base_url="http://test",
    ) as ac:
        yield ac


# ==============================
# FAKE USER REPOSITORY
# ==============================

@pytest_asyncio.fixture
async def user_repo():
    """
    Fake repository para pruebas unitarias
    (no usa base de datos real)
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