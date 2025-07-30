from typing import List, Optional
from fit_tech.app.core.models.workout import Workout
from fit_tech.app.core.models.workout_exercise import WorkoutExercise
from fit_tech.app.core.schemas.workout import WorkoutCreate
from fit_tech.app.db.repositories.workout import WorkoutRepository
from fit_tech.app.core.services.base import BaseService

class WorkoutService(BaseService[Workout, WorkoutCreate]):
    def __init__(self, repository: WorkoutRepository):
        super().__init__(repository)
        self.repository = repository
    
    async def get_with_exercises(self, id: int) -> Optional[Workout]:
        return await self.repository.get_with_exercises(id=id)
    
    async def get_multi_by_user(
        self, *, user_id: int, skip: int = 0, limit: int = 100, 
        type: Optional[str] = None, completed: Optional[bool] = None, planned: Optional[bool] = None, search: Optional[str]  = None
    ) -> List[Workout]:
        return await self.repository.get_multi_by_user(
            user_id=user_id, skip=skip, limit=limit, 
            type=type, completed=completed, planned=planned, search=search
        )
    
    async def create_with_exercises(
        self,
        *,
        workout_in: WorkoutCreate,
        user_id: int
    ) -> Workout:
        data = workout_in.dict(exclude={"exercises"})
        data["user_id"] = user_id

        workout = Workout(**data)
        self.repository.db.add(workout)
        await self.repository.db.commit()
        await self.repository.db.refresh(workout)

        for ex in workout_in.exercises:
            we = WorkoutExercise(
                workout_id=workout.id,
                exercise_id=ex.exercise_id,
                **ex.dict(exclude={"exercise_id"})
            )
            self.repository.db.add(we)

        await self.repository.db.commit()
        return await self.repository.get_with_exercises(id=workout.id)
