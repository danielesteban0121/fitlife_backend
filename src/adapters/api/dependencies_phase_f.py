from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.services.audit_service import AuditService
from src.application.services.notification_service import NotificationService
from src.application.use_cases.auth.change_password import ChangePassword
from src.application.use_cases.auth.reset_password import ResetPassword
from src.application.use_cases.auth.reset_password_request import ResetPasswordRequest
from src.application.use_cases.instructors.assign_instructor import AssignInstructor

# Use Cases - Instructors
from src.application.use_cases.instructors.list_instructors import ListInstructors
from src.application.use_cases.instructors.rate_instructor import RateInstructor
from src.application.use_cases.messages.get_messages import GetMessages

# Use Cases - Messages
from src.application.use_cases.messages.send_message import SendMessage

# Use Cases - Nutrition
from src.application.use_cases.nutrition.create_nutrition_plan import CreateNutritionPlan
from src.application.use_cases.nutrition.get_active_nutrition_plan import GetActiveNutritionPlan
from src.application.use_cases.training.assign_routine import AssignRoutine
from src.application.use_cases.training.complete_workout import CompleteWorkout

# Use Cases - Training
from src.application.use_cases.training.create_routine import CreateRoutine
from src.infrastructure.database.connection import get_db

# Email & Notifications
from src.infrastructure.email.smtp_email_service import SMTPEmailService

# Repositories
from src.infrastructure.repositories.sqlalchemy_instructor_repository import (
    SQLAlchemyInstructorRepository,
)
from src.infrastructure.repositories.sqlalchemy_message_repository import (
    SQLAlchemyMessageRepository,
)
from src.infrastructure.repositories.sqlalchemy_nutrition_repository import (
    SQLAlchemyNutritionRepository,
)
from src.infrastructure.repositories.sqlalchemy_training_repository import (
    SQLAlchemyTrainingRepository,
)
from src.infrastructure.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository


def get_notification_service(db: AsyncSession = Depends(get_db)) -> NotificationService:
    msg_repo = SQLAlchemyMessageRepository(db)
    # Mocking email service constructor, en prod usar env vars
    email_service = SMTPEmailService(
        "smtp.example.com", 587, "user", "pass", "no-reply@fitlife.com"
    )
    return NotificationService(msg_repo, email_service)


# --- Instructors ---
def get_list_instructors(db: AsyncSession = Depends(get_db)) -> ListInstructors:
    return ListInstructors(SQLAlchemyInstructorRepository(db))


def get_assign_instructor(db: AsyncSession = Depends(get_db)) -> AssignInstructor:
    return AssignInstructor(SQLAlchemyInstructorRepository(db), SQLAlchemyUserRepository(db))


def get_rate_instructor(db: AsyncSession = Depends(get_db)) -> RateInstructor:
    return RateInstructor(SQLAlchemyInstructorRepository(db))


# --- Training ---
def get_create_routine(db: AsyncSession = Depends(get_db)) -> CreateRoutine:
    return CreateRoutine(SQLAlchemyTrainingRepository(db))


def get_assign_routine(
    db: AsyncSession = Depends(get_db),
    notif: NotificationService = Depends(get_notification_service),
) -> AssignRoutine:
    return AssignRoutine(SQLAlchemyTrainingRepository(db), notif)


def get_complete_workout(db: AsyncSession = Depends(get_db)) -> CompleteWorkout:
    return CompleteWorkout(SQLAlchemyTrainingRepository(db), SQLAlchemyUserRepository(db))


# --- Nutrition ---
def get_create_nutrition_plan(
    db: AsyncSession = Depends(get_db),
    notif: NotificationService = Depends(get_notification_service),
) -> CreateNutritionPlan:
    return CreateNutritionPlan(SQLAlchemyNutritionRepository(db))


def get_get_active_nutrition_plan(db: AsyncSession = Depends(get_db)) -> GetActiveNutritionPlan:
    return GetActiveNutritionPlan(SQLAlchemyNutritionRepository(db))


# --- Messages ---
def get_send_message(db: AsyncSession = Depends(get_db)) -> SendMessage:
    return SendMessage(SQLAlchemyMessageRepository(db), SQLAlchemyUserRepository(db))


def get_get_messages(db: AsyncSession = Depends(get_db)) -> GetMessages:
    return GetMessages(SQLAlchemyMessageRepository(db))


# ─── Physical Records ────────────────────────────────────────────────────────
from src.application.use_cases.physical_records.create_physical_record import CreatePhysicalRecord  # noqa: E402
from src.application.use_cases.physical_records.get_physical_history import GetPhysicalHistory  # noqa: E402
from src.infrastructure.repositories.sqlalchemy_physical_record_repository import (  # noqa: E402
    SQLAlchemyPhysicalRecordRepository,
)


def get_create_physical_record(db: AsyncSession = Depends(get_db)) -> CreatePhysicalRecord:
    return CreatePhysicalRecord(SQLAlchemyPhysicalRecordRepository(db))


def get_get_physical_history(db: AsyncSession = Depends(get_db)) -> GetPhysicalHistory:
    return GetPhysicalHistory(SQLAlchemyPhysicalRecordRepository(db))


# ─── Assessment Questions ───────────────────────────────────────────────────
from src.application.use_cases.assessments.get_assessment_history import GetAssessmentHistory  # noqa: E402
from src.application.use_cases.assessments.get_assessment_questions import GetAssessmentQuestions  # noqa: E402
from src.infrastructure.repositories.sqlalchemy_assessment_repository import SQLAlchemyAssessmentRepository # noqa: E402

def get_get_assessment_history(db: AsyncSession = Depends(get_db)) -> GetAssessmentHistory:
    return GetAssessmentHistory(SQLAlchemyAssessmentRepository(db))

def get_get_assessment_questions(db: AsyncSession = Depends(get_db)) -> GetAssessmentQuestions:
    return GetAssessmentQuestions(SQLAlchemyAssessmentRepository(db))


# ─── User Profile Use Cases ──────────────────────────────────────────────────

from src.application.use_cases.users.get_user_profile import GetUserProfile  # noqa: E402
from src.application.use_cases.users.update_user_profile import UpdateUserProfile  # noqa: E402
from src.application.use_cases.users.get_profile_audit_log import GetProfileAuditLog  # noqa: E402


def get_audit_service(db: AsyncSession = Depends(get_db)) -> AuditService:
    return AuditService(SQLAlchemyUserRepository(db))


def get_get_user_profile(
    db: AsyncSession = Depends(get_db),
    audit: AuditService = Depends(get_audit_service),
) -> GetUserProfile:
    return GetUserProfile(SQLAlchemyUserRepository(db), audit)


def get_update_user_profile(
    db: AsyncSession = Depends(get_db),
    audit: AuditService = Depends(get_audit_service),
) -> UpdateUserProfile:
    return UpdateUserProfile(SQLAlchemyUserRepository(db), audit)


def get_get_profile_audit_log(
    audit: AuditService = Depends(get_audit_service),
) -> GetProfileAuditLog:
    return GetProfileAuditLog(audit)


# ─── Auth: Password Flows ────────────────────────────────────────────────────
from src.infrastructure.security.bcrypt_password_hasher import BCryptPasswordHasher  # noqa: E402


def get_change_password(db: AsyncSession = Depends(get_db)) -> ChangePassword:
    return ChangePassword(SQLAlchemyUserRepository(db), BCryptPasswordHasher())


def get_reset_password_request(db: AsyncSession = Depends(get_db)) -> ResetPasswordRequest:
    email_service = SMTPEmailService("smtp.example.com", 587, "user", "pass", "no-reply@fitlife.com")
    return ResetPasswordRequest(SQLAlchemyUserRepository(db), email_service)


def get_reset_password() -> ResetPassword:
    return ResetPassword(BCryptPasswordHasher())

