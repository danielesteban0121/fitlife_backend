from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.connection import get_db

# Repositories
from src.infrastructure.repositories.sqlalchemy_instructor_repository import (
    SQLAlchemyInstructorRepository,
)
from src.infrastructure.repositories.sqlalchemy_training_repository import (
    SQLAlchemyTrainingRepository,
)
from src.infrastructure.repositories.sqlalchemy_nutrition_repository import (
    SQLAlchemyNutritionRepository,
)
from src.infrastructure.repositories.sqlalchemy_message_repository import (
    SQLAlchemyMessageRepository,
)
from src.infrastructure.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository

# Email & Notifications
from src.infrastructure.email.smtp_email_service import SMTPEmailService
from src.application.services.notification_service import NotificationService

# Use Cases - Instructors
from src.application.use_cases.instructors.list_instructors import ListInstructors
from src.application.use_cases.instructors.assign_instructor import AssignInstructor
from src.application.use_cases.instructors.rate_instructor import RateInstructor

# Use Cases - Training
from src.application.use_cases.training.create_routine import CreateRoutine
from src.application.use_cases.training.assign_routine import AssignRoutine
from src.application.use_cases.training.complete_workout import CompleteWorkout

# Use Cases - Nutrition
from src.application.use_cases.nutrition.create_nutrition_plan import CreateNutritionPlan
from src.application.use_cases.nutrition.get_active_nutrition_plan import GetActiveNutritionPlan

# Use Cases - Messages
from src.application.use_cases.messages.send_message import SendMessage
from src.application.use_cases.messages.get_messages import GetMessages


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
    return CreateRoutine(
        SQLAlchemyTrainingRepository(db),
        SQLAlchemyUserRepository(db),
        SQLAlchemyInstructorRepository(db),
    )


def get_assign_routine(
    db: AsyncSession = Depends(get_db),
    notif: NotificationService = Depends(get_notification_service),
) -> AssignRoutine:
    return AssignRoutine(SQLAlchemyTrainingRepository(db), SQLAlchemyUserRepository(db), notif)


def get_complete_workout(db: AsyncSession = Depends(get_db)) -> CompleteWorkout:
    return CompleteWorkout(SQLAlchemyTrainingRepository(db), SQLAlchemyUserRepository(db))


# --- Nutrition ---
def get_create_nutrition_plan(
    db: AsyncSession = Depends(get_db),
    notif: NotificationService = Depends(get_notification_service),
) -> CreateNutritionPlan:
    return CreateNutritionPlan(
        SQLAlchemyNutritionRepository(db),
        SQLAlchemyUserRepository(db),
        SQLAlchemyInstructorRepository(db),
        notif,
    )


def get_get_active_nutrition_plan(db: AsyncSession = Depends(get_db)) -> GetActiveNutritionPlan:
    return GetActiveNutritionPlan(SQLAlchemyNutritionRepository(db))


# --- Messages ---
def get_send_message(db: AsyncSession = Depends(get_db)) -> SendMessage:
    return SendMessage(SQLAlchemyMessageRepository(db), SQLAlchemyUserRepository(db))


def get_get_messages(db: AsyncSession = Depends(get_db)) -> GetMessages:
    return GetMessages(SQLAlchemyMessageRepository(db))
