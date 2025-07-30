from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from datetime import timedelta
from fit_tech.app.core.schemas.reminder import Reminder as ReminderSchema, ReminderCreate
from fit_tech.app.core.services.reminder import ReminderService
from fit_tech.app.api.dependencies import get_reminder_service, CurrentUser

router = APIRouter(tags=["reminders"])


@router.get("/", response_model=List[ReminderSchema])
async def list_reminders(
    current_user: CurrentUser,
    service: ReminderService = Depends(get_reminder_service),
):
    return await service.get_multi_by_user(user_id=current_user.id)


@router.post("/", response_model=ReminderSchema, status_code=status.HTTP_201_CREATED)
async def create_reminder(
    obj_in: ReminderCreate,
    current_user: CurrentUser,
    service: ReminderService = Depends(get_reminder_service),
):
    obj_in.due_at = obj_in.due_at - timedelta(hours=3)

    return await service.create_for_user(user_id=current_user.id, obj_in=obj_in)


@router.get("/{reminder_id}", response_model=ReminderSchema)
async def get_reminder(
    reminder_id: int,
    current_user: CurrentUser,
    service: ReminderService = Depends(get_reminder_service),
):
    reminder = await service.get(reminder_id, user_id=current_user.id)
    if not reminder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Напоминание не найдено"
        )
    return reminder

@router.delete("/{reminder_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reminder(
    reminder_id: int,
    current_user: CurrentUser,
    service: ReminderService = Depends(get_reminder_service),
):
    success = await service.delete(reminder_id, user_id=current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Напоминание не найдено для удаления"
        )
    return None
