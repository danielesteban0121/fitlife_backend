import asyncio
from datetime import datetime, timezone
from uuid import uuid4

from src.domain.entities.user import User
from src.domain.enums.user_role import UserRole
from src.domain.value_objects.email import Email
from src.infrastructure.database.connection import AsyncSessionLocal
from src.infrastructure.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository


async def test():
    async with AsyncSessionLocal() as session:
        repo = SQLAlchemyUserRepository(session)

        # 🔹 Crear usuario
        user = User(
            id=uuid4(),
            email=Email("test@test.com"),
            password_hash="123456",
            role=UserRole.USER,
            is_active=True,
            created_at=datetime.now(timezone.utc),
        )

        print("✅ Guardando usuario...")
        await repo.save(user)

        # 🔹 Buscar usuario
        print("🔍 Buscando usuario...")
        found = await repo.find_by_email(Email("test@test.com"))

        print("\n📦 RESULTADO:")
        print(found)


if __name__ == "__main__":
    asyncio.run(test())
