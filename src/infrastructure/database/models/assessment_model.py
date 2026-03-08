<<<<<<< HEAD
from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import JSON

from src.infrastructure.database.base import Base


class AssessmentModel(Base):

    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    fitness_score = Column(Float, nullable=False)
    answers = Column(JSON, nullable=False)
=======
from sqlalchemy import String, Float, Integer, DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from uuid import uuid4
from datetime import datetime, UTC

from ..base import Base
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
        unique=True,  # Asumimos una evaluación inicial por usuario
    )

    goal: Mapped[FitnessGoal] = mapped_column(Enum(FitnessGoal), nullable=False)
    activity_level: Mapped[ActivityLevel] = mapped_column(Enum(ActivityLevel), nullable=False)
    experience_level: Mapped[ExperienceLevel] = mapped_column(Enum(ExperienceLevel), nullable=False)

    height_cm: Mapped[float] = mapped_column(Float, nullable=False)
    weight_kg: Mapped[float] = mapped_column(Float, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)

    fitness_score: Mapped[float] = mapped_column(Float, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    # Relación de vuelta si la quisiéramos usar en UserModel
    # user = relationship("UserModel", back_populates="assessment")
>>>>>>> a8a4ebf (feat(auth,assessment): implementar flujo completo de autenticación JWT y módulo de valoraciones físicas)
