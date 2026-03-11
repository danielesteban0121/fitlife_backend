from uuid import UUID

from src.domain.entities.training import Routine, Exercise, RoutineExercise, WorkoutLog
from src.infrastructure.database.models.training_models import RoutineModel, ExerciseModel, RoutineExerciseModel, WorkoutLogModel

class TrainingMapper:
    @staticmethod
    def routine_to_domain(model: RoutineModel) -> Routine:
        exercises = [TrainingMapper.routine_exercise_to_domain(ex) for ex in model.exercises] if model.exercises else []
        return Routine(
            id=UUID(model.id),
            user_id=UUID(model.user_id),
            instructor_id=UUID(model.instructor_id),
            title=model.title,
            description=model.description,
            created_at=model.created_at,
            is_active=model.is_active,
            exercises=exercises
        )

    @staticmethod
    def routine_to_model(domain: Routine) -> RoutineModel:
        return RoutineModel(
            id=str(domain.id),
            user_id=str(domain.user_id),
            instructor_id=str(domain.instructor_id),
            title=domain.title,
            description=domain.description,
            created_at=domain.created_at,
            is_active=domain.is_active
        )
    
    @staticmethod
    def routine_exercise_to_domain(model: RoutineExerciseModel) -> RoutineExercise:
        return RoutineExercise(
            exercise_id=UUID(model.exercise_id),
            target_sets=model.target_sets,
            target_reps=model.target_reps,
            rest_seconds=model.rest_seconds,
            notes=model.notes
        )
    
    @staticmethod
    def routine_exercise_to_model(domain: RoutineExercise, routine_id: str) -> RoutineExerciseModel:
        return RoutineExerciseModel(
            routine_id=routine_id,
            exercise_id=str(domain.exercise_id),
            target_sets=domain.target_sets,
            target_reps=domain.target_reps,
            rest_seconds=domain.rest_seconds,
            notes=domain.notes
        )

    @staticmethod
    def exercise_to_domain(model: ExerciseModel) -> Exercise:
        return Exercise(
            id=UUID(model.id),
            name=model.name,
            description=model.description,
            category=model.category,
            video_url=model.video_url
        )

    @staticmethod
    def workout_log_to_domain(model: WorkoutLogModel) -> WorkoutLog:
        return WorkoutLog(
            id=UUID(model.id),
            routine_id=UUID(model.routine_id),
            user_id=UUID(model.user_id),
            completed_at=model.completed_at,
            notes=model.notes,
            duration_minutes=model.duration_minutes
        )

    @staticmethod
    def workout_log_to_model(domain: WorkoutLog) -> WorkoutLogModel:
        return WorkoutLogModel(
            id=str(domain.id),
            routine_id=str(domain.routine_id),
            user_id=str(domain.user_id),
            completed_at=domain.completed_at,
            notes=domain.notes,
            duration_minutes=domain.duration_minutes
        )
