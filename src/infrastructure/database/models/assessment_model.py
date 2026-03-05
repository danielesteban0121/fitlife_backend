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
