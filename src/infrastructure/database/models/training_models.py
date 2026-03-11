from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, Enum, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.entities.training import ExerciseCategory

from ..base import Base

class ExerciseModel(Base):
    __tablename__ = "exercises"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    category: Mapped[ExerciseCategory] = mapped_column(Enum(ExerciseCategory), nullable=False)
    video_url: Mapped[str] = mapped_column(String, nullable=True)

class RoutineModel(Base):
    __tablename__ = "routines"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    instructor_id: Mapped[str] = mapped_column(String, ForeignKey("instructors.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    exercises = relationship("RoutineExerciseModel", back_populates="routine", cascade="all, delete-orphan")

class RoutineExerciseModel(Base):
    __tablename__ = "routine_exercises"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    routine_id: Mapped[str] = mapped_column(String, ForeignKey("routines.id", ondelete="CASCADE"), nullable=False)
    exercise_id: Mapped[str] = mapped_column(String, ForeignKey("exercises.id", ondelete="CASCADE"), nullable=False)
    target_sets: Mapped[int] = mapped_column(Integer, nullable=False)
    target_reps: Mapped[int] = mapped_column(Integer, nullable=False)
    rest_seconds: Mapped[int] = mapped_column(Integer, nullable=False)
    notes: Mapped[str] = mapped_column(String, nullable=True)

    routine = relationship("RoutineModel", back_populates="exercises")
    exercise = relationship("ExerciseModel")

class WorkoutLogModel(Base):
    __tablename__ = "workout_logs"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    routine_id: Mapped[str] = mapped_column(String, ForeignKey("routines.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    completed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    notes: Mapped[str] = mapped_column(String, nullable=True)
    duration_minutes: Mapped[int] = mapped_column(Integer, nullable=True)
