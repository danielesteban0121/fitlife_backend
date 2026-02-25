from sqlalchemy import Column, String, Boolean, DateTime, Enum
from src.infrastructure.database.base import Base
from src.domain.enums.user_role import UserRole


class UserModel(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime)
