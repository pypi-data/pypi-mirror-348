from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional

from fit_tech.app.core.models.exercise import MuscleGroup, Difficulty
from fit_tech.app.core.schemas.workout import Exercise, ExerciseCreate
from fit_tech.app.core.services.exercise import ExerciseService
from fit_tech.app.api.dependencies import get_exercise_service, CurrentUser

router = APIRouter()

@router.get("/", response_model=List[Exercise])
async def get_exercises(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    muscle_group: Optional[MuscleGroup] = None,
    difficulty: Optional[Difficulty] = None,
    exercise_service: ExerciseService = Depends(get_exercise_service),
):
    """
    Получить список упражнений с возможностью фильтрации
    """
    exercises = await exercise_service.get_multi_filtered(
        skip=skip,
        limit=limit,
        search=search,
        muscle_group=muscle_group,
        difficulty=difficulty,
        is_public=True
    )
    return exercises

@router.post("/", response_model=Exercise, status_code=status.HTTP_201_CREATED)
async def create_exercise(
    exercise_in: ExerciseCreate,
    current_user: CurrentUser,
    exercise_service: ExerciseService = Depends(get_exercise_service)
):
    """
    Создать новое упражнение (пользовательское или для админа)
    """
    exercise_in.is_public = exercise_in.is_public if current_user.is_superuser else False
    exercise = await exercise_service.create_with_author(obj_in=exercise_in, author_id=current_user.id)
    return exercise

@router.get("/{exercise_id}", response_model=Exercise)
async def get_exercise(
    exercise_id: int,
    current_user: CurrentUser,
    exercise_service: ExerciseService = Depends(get_exercise_service)
):
    """
    Получить детали упражнения по ID
    """
    exercise = await exercise_service.get(id=exercise_id)
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Упражнение не найдено"
        )
    if not exercise.is_public and exercise.author_id != current_user.id:
         raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Не авторизован для доступа к этому упражнению"
        )
    return exercise

@router.delete("/{exercise_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_exercise(
    exercise_id: int,
    current_user: CurrentUser,
    exercise_service: ExerciseService = Depends(get_exercise_service)
):
    """
    Удалить упражнение
    """
    exercise = await exercise_service.get(id=exercise_id)
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Упражнение не найдено"
        )
    if exercise.author_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Не авторизован для удаления этого упражнения"
        )
        
    await exercise_service.delete(id=exercise_id)
    return None
