from uuid import UUID

from src.domain.entities.instructor import Instructor, InstructorAssignment
from src.infrastructure.database.models.instructor_model import InstructorModel, InstructorAssignmentModel

class InstructorMapper:
    @staticmethod
    def to_domain(model: InstructorModel) -> Instructor:
        return Instructor(
            id=UUID(model.id),
            user_id=UUID(model.user_id),
            certifications=model.certifications,
            specializations=model.specializations,
            average_rating=model.average_rating,
            active_users_count=model.active_users_count
        )

    @staticmethod
    def to_model(domain: Instructor) -> InstructorModel:
        return InstructorModel(
            id=str(domain.id),
            user_id=str(domain.user_id),
            certifications=domain.certifications,
            specializations=domain.specializations,
            average_rating=domain.average_rating,
            active_users_count=domain.active_users_count
        )

class InstructorAssignmentMapper:
    @staticmethod
    def to_domain(model: InstructorAssignmentModel) -> InstructorAssignment:
        return InstructorAssignment(
            id=UUID(model.id),
            user_id=UUID(model.user_id),
            instructor_id=UUID(model.instructor_id),
            is_active=model.is_active,
            assigned_at=model.assigned_at,
            ended_at=model.ended_at
        )

    @staticmethod
    def to_model(domain: InstructorAssignment) -> InstructorAssignmentModel:
        return InstructorAssignmentModel(
            id=str(domain.id),
            user_id=str(domain.user_id),
            instructor_id=str(domain.instructor_id),
            is_active=domain.is_active,
            assigned_at=domain.assigned_at,
            ended_at=domain.ended_at
        )
