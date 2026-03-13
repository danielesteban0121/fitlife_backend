from datetime import date

from sqlalchemy import Date, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from ..base import Base


class UserProfileModel(Base):
    __tablename__ = "user_profiles"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(36), index=True)
    full_name: Mapped[str] = mapped_column(String(255))
    date_of_birth: Mapped[date | None] = mapped_column(Date, nullable=True)
    height_cm: Mapped[float | None] = mapped_column(Float, nullable=True)
