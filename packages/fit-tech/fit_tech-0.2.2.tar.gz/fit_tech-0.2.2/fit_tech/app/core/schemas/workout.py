from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime

from fit_tech.app.core.models.exercise import MuscleGroup, Difficulty
from fit_tech.app.core.models.workout import WorkoutType


class ExerciseBase(BaseModel):
    name: str
    description: Optional[str] = None
    muscle_group: MuscleGroup
    difficulty: Difficulty
    equipment: Optional[str] = None
    instructions: Optional[str] = None
    video_url: Optional[str] = None
    image_url: Optional[str] = None
    calories_per_hour: Optional[int] = None
    is_public: Optional[bool] = True

class ExerciseCreate(ExerciseBase):
    pass

class ExerciseInDBBase(ExerciseBase):
    id: int
    author_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

class Exercise(ExerciseInDBBase):
    pass

class WorkoutExerciseBase(BaseModel):
    exercise_id: int
    sets: Optional[int] = 3
    reps: Optional[int] = 10
    weight: Optional[float] = None
    rest_time: Optional[int] = None
    order: Optional[int] = 0

class WorkoutExerciseCreate(WorkoutExerciseBase):
    pass

class WorkoutExerciseInDBBase(WorkoutExerciseBase):
    id: int
    workout_id: int
    model_config = ConfigDict(from_attributes=True)

class WorkoutExercise(WorkoutExerciseInDBBase):
    exercise: Optional[Exercise] = None


class WorkoutBase(BaseModel):
    name: str
    description: Optional[str] = None
    type: Optional[WorkoutType] = WorkoutType.OTHER
    duration: Optional[int] = None
    calories_burned: Optional[int] = None
    scheduled_date: Optional[datetime] = None

class WorkoutCreate(WorkoutBase):
    exercises: List[WorkoutExerciseCreate] = []

class WorkoutInDBBase(WorkoutBase):
    id: int
    user_id: int
    completed: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)

class Workout(WorkoutInDBBase):
    exercises: List[WorkoutExercise] = []

class WorkoutTemplate(BaseModel):
    name: str
    description: Optional[str] = None
    type: WorkoutType
    difficulty: Difficulty
    goal: str = Field(..., description="Цель: strength, cardio, weight_loss, muscle_gain, endurance")
    duration: int = Field(..., description="Примерная продолжительность в минутах")
