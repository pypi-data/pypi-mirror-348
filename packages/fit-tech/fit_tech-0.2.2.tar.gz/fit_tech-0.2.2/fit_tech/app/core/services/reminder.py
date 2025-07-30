from typing import List, Optional
from datetime import datetime, timezone

from fit_tech.app.core.models.reminder import Reminder, RepeatType
from fit_tech.app.core.schemas.reminder import ReminderCreate
from fit_tech.app.db.repositories.reminder import ReminderRepository
from fit_tech.app.core.services.base import BaseService

class ReminderService(BaseService[Reminder, ReminderCreate]):
    def __init__(self, repository: ReminderRepository):
        super().__init__(repository)
    
    async def get_multi_by_user(
        self, *, 
        user_id: int, 
        skip: int = 0, 
        limit: int = 100, 
        is_active: Optional[bool] = None,
        repeat_type: Optional[RepeatType] = None
    ) -> List[Reminder]:
        return await self.repository.get_multi_by_user(
            user_id=user_id,
            skip=skip,
            limit=limit,
            is_active=is_active,
            repeat_type=repeat_type
        )


    async def delete(self, reminder_id: int, user_id: int) -> bool:
        return await self.repository.delete(reminder_id=reminder_id, user_id=user_id)
    
    async def create_for_user(self, *, obj_in: ReminderCreate, user_id: int) -> Reminder:
        return await self.repository.create_for_user(obj_in=obj_in, user_id=user_id)

    async def get_due_reminders_for_notification(self, current_time: datetime) -> List[Reminder]:
        return await self.repository.get_due_reminders_for_notification(current_time=current_time)

    async def mark_as_sent(self, reminder_id: int) -> Optional[Reminder]:
        return await self.repository.mark_as_sent(reminder_id=reminder_id)
