from sqlalchemy import String, Float, Integer, DateTime, Enum as SAEnum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from uuid import uuid4
from datetime import datetime, UTC

from src.infrastructure.database.base import Base
from src.domain.entities.assessment import FitnessGoal, ActivityLevel, ExperienceLevel


class AssessmentModel(Base):
    __tablename__ = "assessments"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    user_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,  # Una evaluación inicial por usuario
    )

    goal: Mapped[FitnessGoal] = mapped_column(SAEnum(FitnessGoal), nullable=False)
    activity_level: Mapped[ActivityLevel] = mapped_column(SAEnum(ActivityLevel), nullable=False)
    experience_level: Mapped[ExperienceLevel] = mapped_column(
        SAEnum(ExperienceLevel), nullable=False
    )

    height_cm: Mapped[float] = mapped_column(Float, nullable=False)
    weight_kg: Mapped[float] = mapped_column(Float, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)

    fitness_score: Mapped[float] = mapped_column(Float, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )
