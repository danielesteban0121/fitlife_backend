from typing import List

from pydantic import BaseModel


class AnswerSchema(BaseModel):
    question_id: int
    answer: int


class SubmitAssessmentSchema(BaseModel):
    user_id: int
    answers: List[AnswerSchema]
