from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from fit_tech.app.core.models.reminder import RepeatType 


class ReminderBase(BaseModel):
    title: str
    description: Optional[str] = None
    reminder_time: datetime
    repeat_type: RepeatType = RepeatType.NONE
    rrule: Optional[str] = None
    is_active: bool = True
    notify_in_telegram: bool = False

class ReminderCreate(BaseModel):
    text: str
    due_at: datetime
    notify_in_telegram: bool
    description: Optional[str] = None
    repeat_type: RepeatType = RepeatType.NONE
    rrule: Optional[str] = None
    is_active: bool = True

class ReminderInDBBase(ReminderBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    is_sent: Optional[bool] = False
    model_config = ConfigDict(from_attributes=True)

class Reminder(ReminderInDBBase):
    pass

