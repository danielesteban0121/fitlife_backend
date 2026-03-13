import os
import sys
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.config.settings import settings
from src.infrastructure.database.base import Base

# Construcción de la URL para MySQL usando aiomysql
DATABASE_URL = (
    f"mysql+aiomysql://{settings.DB_USER}:{settings.DB_PASSWORD}@"
    f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)

# SQLite fallback solo para tests si no se define una URL de test específica
if "pytest" in sys.modules or os.environ.get("TESTING") == "1":
    DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,  # Recomendado para MySQL para evitar desconexiones
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


# 🔹 Dependency principal
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


# 🔹 Alias para compatibilidad con código existente
get_db = get_session


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
