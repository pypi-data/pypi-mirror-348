from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from datetime import datetime

from fit_tech.app.core.models.reminder import Reminder, RepeatType
from fit_tech.app.core.schemas.reminder import ReminderCreate
from fit_tech.app.db.repositories.base import BaseRepository

class ReminderRepository(BaseRepository[Reminder, ReminderCreate]):
    def __init__(self, db: Session):
        super().__init__(Reminder, db)

    async def get_multi_by_user(
        self, *,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[bool] = None,
        repeat_type: Optional[RepeatType] = None
    ) -> List[Reminder]:
        query = select(self.model).where(self.model.user_id == user_id)

        if is_active is not None:
            query = query.where(self.model.is_active == is_active)

        if repeat_type:
            query = query.where(self.model.repeat_type == repeat_type)

        query = query.order_by(self.model.reminder_time).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def create_for_user(self, *, obj_in: ReminderCreate, user_id: int) -> Reminder:
        """
        Создает напоминания, сопоставляя ReminderCreate схему с
        моделью Reminder.
        """
        db_reminder = self.model(
            title=obj_in.text,
            reminder_time=obj_in.due_at,
            notify_in_telegram=obj_in.notify_in_telegram,
            description=obj_in.description,
            repeat_type=obj_in.repeat_type,
            rrule=obj_in.rrule,
            is_active=obj_in.is_active,
            user_id=user_id,
            is_sent=False
        )
        self.db.add(db_reminder)
        await self.db.commit()
        await self.db.refresh(db_reminder)
        return db_reminder

    async def create(self, *, obj_in: ReminderCreate, user_id: Optional[int] = None) -> Reminder:
        if user_id is None:
            raise ValueError("user_id необходим для создания напоминания")

        db_reminder = self.model(
            title=obj_in.text,
            reminder_time=obj_in.due_at,
            notify_in_telegram=obj_in.notify_in_telegram,
            description=obj_in.description,
            repeat_type=obj_in.repeat_type,
            rrule=obj_in.rrule,
            is_active=obj_in.is_active,
            user_id=user_id,
            is_sent=False
        )
        self.db.add(db_reminder)
        await self.db.commit()
        await self.db.refresh(db_reminder)
        return db_reminder
    
    async def delete(self, reminder_id: int, user_id: int) -> bool:
        """
        Удаляет напоминание по его или пользовательскому айдишнику
        """
        query = select(self.model).where(
            self.model.id == reminder_id,
            self.model.user_id == user_id
        )
        result = await self.db.execute(query)
        reminder = result.scalar_one_or_none()

        if reminder:
            await self.db.delete(reminder)
            await self.db.commit()
            return True
        return False

    async def get_due_reminders_for_notification(self, current_time: datetime) -> List[Reminder]:
        """
        Извлекает активные и неотправленые напоминания
        """
        query = (select(self.model)
            .options(selectinload(Reminder.user))
            .where(
                Reminder.reminder_time <= current_time,
                Reminder.is_sent == False,
                Reminder.is_active == True,
                Reminder.notify_in_telegram == True,
            ))

        result = await self.db.execute(query)
        return result.scalars().all()

    async def mark_as_sent(self, reminder_id: int) -> Optional[Reminder]:
        """
        Помечает напоминание как отправленное
        """
        query = select(self.model).where(self.model.id == reminder_id)
        result = await self.db.execute(query)
        reminder = result.scalar_one_or_none()

        if reminder:
            reminder.is_sent = True
            await self.db.commit()
            await self.db.refresh(reminder)
            return reminder
        return None

