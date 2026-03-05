import pytest_asyncio

from src.infrastructure.database.base import Base
from src.infrastructure.database.connection import engine


@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database():

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)