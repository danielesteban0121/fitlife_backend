from sqlalchemy import Boolean, Column, DateTime, Enum, String

from src.domain.enums.user_role import UserRole
from src.infrastructure.database.base import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime)
