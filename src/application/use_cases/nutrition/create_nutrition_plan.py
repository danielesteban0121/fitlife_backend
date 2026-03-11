import uuid
from src.domain.entities.nutrition import NutritionPlan, DailyMeal
from src.domain.repositories.nutrition_repository import NutritionRepository
from src.domain.repositories.user_repository import UserRepository
from src.domain.repositories.instructor_repository import InstructorRepository
from src.domain.exceptions.base import DomainException
from src.application.dtos.nutrition_dtos import CreateNutritionPlanRequestDTO, CreateNutritionPlanResponseDTO

class CreateNutritionPlan:
    def __init__(
        self,
        nutrition_repository: NutritionRepository,
        user_repository: UserRepository,
        instructor_repository: InstructorRepository,
        notification_service=None
    ):
        self.nutrition_repository = nutrition_repository
        self.user_repository = user_repository
        self.instructor_repository = instructor_repository
        self.notification_service = notification_service

    async def execute(self, request: CreateNutritionPlanRequestDTO) -> CreateNutritionPlanResponseDTO:
        user = await self.user_repository.find_by_id(request.user_id)
        if not user:
            raise DomainException(f"User {request.user_id} no encontrado")

        instructor = await self.instructor_repository.find_by_id(request.instructor_id)
        if not instructor:
            raise DomainException(f"Instructor {request.instructor_id} no encontrado")

        # Invalidate previous active plan
        active_plan = await self.nutrition_repository.get_active_plan_by_user(request.user_id)
        if active_plan:
            active_plan.is_active = False
            await self.nutrition_repository.save_plan(active_plan)

        meals_domain = [
            DailyMeal(
                id=uuid.uuid4(),
                meal_type=m.meal_type,
                description=m.description,
                calories=m.calories,
                macros=m.macros
            )
            for m in request.meals
        ]

        plan = NutritionPlan(
            id=uuid.uuid4(),
            user_id=request.user_id,
            instructor_id=request.instructor_id,
            target_calories=request.target_calories,
            macro_distribution=request.macro_distribution,
            start_date=request.start_date,
            end_date=request.end_date,
            meals=meals_domain
        )

        saved_plan = await self.nutrition_repository.save_plan(plan)

        # Notify user if service is injected
        if self.notification_service:
            await self.notification_service.send_assignment_notification(
                user_id=request.user_id,
                assignment_type="plan de nutrición",
                details={"target_calories": saved_plan.target_calories}
            )

        return CreateNutritionPlanResponseDTO(
            plan_id=saved_plan.id,
            created_at=saved_plan.created_at,
            message="Plan de nutrición creado y asignado exitosamente"
        )
