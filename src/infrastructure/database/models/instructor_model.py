from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, Float, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base


class InstructorModel(Base):
    __tablename__ = "instructors"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id: Mapped[str] = mapped_column(
        String, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    certifications: Mapped[list] = mapped_column(JSON, default=list)
    specializations: Mapped[list] = mapped_column(JSON, default=list)
    average_rating: Mapped[float] = mapped_column(Float, default=0.0)
    active_users_count: Mapped[int] = mapped_column(Integer, default=0)

    user = relationship("UserModel", backref="instructor_profile")


class InstructorAssignmentModel(Base):
    __tablename__ = "instructor_assignments"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id: Mapped[str] = mapped_column(
        String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    instructor_id: Mapped[str] = mapped_column(
        String, ForeignKey("instructors.id", ondelete="CASCADE"), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    assigned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
    ended_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    user = relationship("UserModel", backref="instructor_assignments")
    instructor = relationship("InstructorModel", backref="assignments")
