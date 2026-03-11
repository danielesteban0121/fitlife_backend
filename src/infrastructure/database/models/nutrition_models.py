from datetime import UTC, date, datetime
from uuid import uuid4

from sqlalchemy import JSON, Boolean, Date, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.entities.nutrition import MealType

from ..base import Base


class NutritionPlanModel(Base):
    __tablename__ = "nutrition_plans"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id: Mapped[str] = mapped_column(
        String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    instructor_id: Mapped[str] = mapped_column(
        String, ForeignKey("instructors.id", ondelete="CASCADE"), nullable=False
    )
    target_calories: Mapped[int] = mapped_column(Integer, nullable=False)
    macro_distribution: Mapped[dict] = mapped_column(JSON, default=dict)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    meals = relationship("DailyMealModel", back_populates="plan", cascade="all, delete-orphan")


class DailyMealModel(Base):
    __tablename__ = "daily_meals"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    plan_id: Mapped[str] = mapped_column(
        String, ForeignKey("nutrition_plans.id", ondelete="CASCADE"), nullable=False
    )
    meal_type: Mapped[MealType] = mapped_column(Enum(MealType), nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    calories: Mapped[int] = mapped_column(Integer, nullable=False)
    macros: Mapped[dict] = mapped_column(JSON, default=dict)

    plan = relationship("NutritionPlanModel", back_populates="meals")
