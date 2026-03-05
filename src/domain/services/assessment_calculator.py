from typing import List

from src.domain.entities.assessment import AssessmentAnswer


class AssessmentCalculator:

    @staticmethod
    def calculate(answers: List[AssessmentAnswer]) -> float:

        if not answers:
            raise ValueError("Assessment requires answers")

        total = 0

        for answer in answers:

            if answer.answer < 1 or answer.answer > 5:
                raise ValueError("Answer must be between 1 and 5")

            total += answer.answer

        average = total / len(answers)

        return round(average * 20, 2)
