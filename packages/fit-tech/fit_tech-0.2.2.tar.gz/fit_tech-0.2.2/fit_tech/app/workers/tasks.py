import asyncio
from fit_tech.app.workers.celery_app import celery_app
from datetime import datetime, timezone
import os
import logging
import requests
from fit_tech.app.workers.celery_app import celery_app
from fit_tech.app.db.repositories.reminder import ReminderRepository
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from fit_tech.app.db.session import ASYNC_DATABASE_URL

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
logger = logging.getLogger(__name__)

@celery_app.task
def send_due_telegram_reminders():
    async def _send_all():
        sent_count   = 0
        failed_count = 0

        engine = create_async_engine(
            ASYNC_DATABASE_URL,
            echo=False,
            future=True,
        )
        LocalSession = sessionmaker(
            bind=engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

        async with LocalSession() as session:
            reminder_repo = ReminderRepository(session)
            now = datetime.now(timezone.utc)
            due = await reminder_repo.get_due_reminders_for_notification(current_time=now)
            for reminder in due:
                try:
                    if not TELEGRAM_BOT_TOKEN:
                        raise RuntimeError("TELEGRAM_BOT_TOKEN не задан")
                    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
                    payload = {
                        "chat_id": reminder.user.telegram_id,
                        "text": f"🔔 {reminder.title}" + f"\n{reminder.description}"
                    }
                    requests.post(url, json=payload, timeout=10)
                    await reminder_repo.mark_as_sent(reminder.id)
                    sent_count += 1
                except Exception as e:
                    logger.error(f"Error sending reminder {reminder.id}: {e}", exc_info=True)
                    failed_count += 1
            return len(due)
    
    loop = asyncio.new_event_loop()
    try:
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(_send_all())
    finally:
        loop.close()
    return result
