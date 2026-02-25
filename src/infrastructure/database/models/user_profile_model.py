from sqlalchemy import Column, String, Float, Date, ForeignKey
from src.infrastructure.database.base import Base


class UserProfileModel(Base):
    __tablename__ = "user_profiles"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"))
    full_name = Column(String)
    date_of_birth = Column(Date)
    height_cm = Column(Float)
