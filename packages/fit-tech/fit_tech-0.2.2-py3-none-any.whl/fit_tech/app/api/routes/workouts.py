from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional

from fit_tech.app.core.schemas.workout import WorkoutCreate, Workout
from fit_tech.app.core.services.workout import WorkoutService
from fit_tech.app.api.dependencies import get_workout_service, CurrentUser

router = APIRouter()

@router.post("/", response_model=Workout, status_code=status.HTTP_201_CREATED)
async def create_workout(
    current_user: CurrentUser,
    workout_in: WorkoutCreate,
    workout_service: WorkoutService = Depends(get_workout_service)
):
    """
    Создать новую тренировку для текущего пользователя
    """
    
    workout = await workout_service.create_with_exercises(workout_in=workout_in, user_id=current_user.id)
    return workout

@router.get("/", response_model=List[Workout])
async def get_workouts(
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
    type: Optional[str] = None,
    completed: Optional[bool] = None,
    planned: Optional[bool] = None,
    search: Optional[str]  = None,
    workout_service: WorkoutService = Depends(get_workout_service)
):
    """
    Получить список тренировок текущего пользователя с возможностью фильтрации
    """
    workouts = await workout_service.get_multi_by_user(
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        type=type,
        completed=completed,
        planned=planned,
        search=search
    )
    return workouts

@router.get("/{workout_id}", response_model=Workout)
async def get_workout(
    current_user: CurrentUser,
    workout_id: int,
    workout_service: WorkoutService = Depends(get_workout_service)
) -> Workout:
    """
    Получить детали конкретной тренировки
    """
    workout = await workout_service.get_with_exercises(id=workout_id)
    if not workout or workout.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout not found"
        )
    return workout

@router.delete("/{workout_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workout(
    current_user: CurrentUser,
    workout_id: int,
    workout_service: WorkoutService = Depends(get_workout_service)
):
    """
    Удалить тренировку
    """
    workout = await workout_service.get(id=workout_id)
    if not workout or workout.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout not found"
        )
    
    await workout_service.delete(id=workout_id)
    return None
