from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import or_

from fit_tech.app.core.models.workout import Workout
from fit_tech.app.core.models.workout_exercise import WorkoutExercise
from fit_tech.app.core.schemas.workout import WorkoutCreate
from fit_tech.app.db.repositories.base import BaseRepository

class WorkoutRepository(BaseRepository[Workout, WorkoutCreate]):
    def __init__(self, db: Session):
        super().__init__(Workout, db)
    
    async def get_with_exercises(self, id: int) -> Optional[Workout]:
        query = select(Workout).where(Workout.id == id).options(
            selectinload(Workout.exercises)
            .selectinload(WorkoutExercise.exercise)
        )
        result = await self.db.execute(query)
        workout = result.scalars().first()
        return workout
    
    async def get_multi_by_user(
        self, *, user_id: int, skip: int = 0, limit: int = 100, 
        type: Optional[str] = None, completed: Optional[bool] = None, planned: Optional[bool] = None, search: Optional[str] = None
    ) -> List[Workout]:
        query = select(Workout).where(Workout.user_id == user_id).options(
            selectinload(Workout.exercises).selectinload(WorkoutExercise.exercise))
        
        if type:
            query = query.where(Workout.type == type)
        if completed is not None:
            query = query.where(Workout.completed == completed)
        if planned is not None:
            if planned:
                query = query.where(Workout.scheduled_date.isnot(None))
            else:
                query = query.where(Workout.scheduled_date.is_(None))
        if search:
            pattern = f"%{search}%"
            query = query.where(
                or_(
                    Workout.name.ilike(pattern),
                    Workout.description.ilike(pattern),
                )
            )
        
        query = query.order_by(Workout.created_at.desc()).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()
