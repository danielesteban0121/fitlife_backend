from typing import Any, Dict, List, Optional
from uuid import uuid4

from sqlalchemy import JSON, Boolean, Enum, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.entities.assessment_question import QuestionCategory, QuestionType
from src.infrastructure.database.base import Base


class AssessmentQuestionModel(Base):
    __tablename__ = "assessment_questions"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    question_type: Mapped[QuestionType] = mapped_column(
        Enum(QuestionType),
        nullable=False,
    )

    category: Mapped[QuestionCategory] = mapped_column(
        Enum(QuestionCategory),
        nullable=False,
    )

    label: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    weight: Mapped[float] = mapped_column(
        Float,
        default=1.0,
        nullable=False,
    )

    display_order: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    constraints: Mapped[Dict[str, Any]] = mapped_column(
        JSON,
        default=dict,
        nullable=False,
    )

    options: Mapped[Optional[List[str]]] = mapped_column(
        JSON,
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
