import asyncio

from src.infrastructure.database.base import Base
from src.infrastructure.database.connection import engine

# IMPORTANTE: importar modelos para que SQLAlchemy los registre
from src.infrastructure.database.models.user_model import UserModel  # noqa: F401
from src.infrastructure.database.models.user_profile_model import UserProfileModel  # noqa: F401


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(init_db())
