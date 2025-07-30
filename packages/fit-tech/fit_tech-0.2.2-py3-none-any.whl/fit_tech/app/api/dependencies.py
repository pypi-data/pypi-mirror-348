from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from fit_tech.app.db.session import get_db
from fit_tech.app.db.repositories.user import UserRepository
from fit_tech.app.db.repositories.workout import WorkoutRepository
from fit_tech.app.db.repositories.exercise import ExerciseRepository
from fit_tech.app.db.repositories.recipe import RecipeRepository
from fit_tech.app.db.repositories.ingredient import IngredientRepository
from fit_tech.app.db.repositories.reminder import ReminderRepository

from fit_tech.app.core.services.user import UserService
from fit_tech.app.core.services.workout import WorkoutService
from fit_tech.app.core.services.exercise import ExerciseService
from fit_tech.app.core.services.recipe import RecipeService
from fit_tech.app.core.services.ingredient import IngredientService
from fit_tech.app.core.services.reminder import ReminderService

from fit_tech.app.core.security import get_current_active_user
from fit_tech.app.core.models.user import User

DbSession = Annotated[AsyncSession, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_active_user)]

def get_user_repository(db: DbSession) -> UserRepository:
    return UserRepository(db)

def get_workout_repository(db: DbSession) -> WorkoutRepository:
    return WorkoutRepository(db)

def get_exercise_repository(db: DbSession) -> ExerciseRepository:
    return ExerciseRepository(db)

def get_recipe_repository(db: DbSession) -> RecipeRepository:
    return RecipeRepository(db)

def get_ingredient_repository(db: DbSession) -> IngredientRepository:
    return IngredientRepository(db)

def get_reminder_repository(db: DbSession) -> ReminderRepository:
    return ReminderRepository(db)


def get_user_service(
    repository: UserRepository = Depends(get_user_repository)
) -> UserService:
    return UserService(repository)

def get_workout_service(
    repository: WorkoutRepository = Depends(get_workout_repository)
) -> WorkoutService:
    return WorkoutService(repository)

def get_exercise_service(
    repository: ExerciseRepository = Depends(get_exercise_repository)
) -> ExerciseService:
    return ExerciseService(repository)

def get_recipe_service(
    repository: RecipeRepository = Depends(get_recipe_repository)
) -> RecipeService:
    return RecipeService(repository)

def get_ingredient_service(
    repository: IngredientRepository = Depends(get_ingredient_repository)
) -> IngredientService:
    return IngredientService(repository)

def get_reminder_service(
    repository: ReminderRepository = Depends(get_reminder_repository)
) -> ReminderService:
    return ReminderService(repository)

