from celery import Celery
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

celery_app = Celery(
    "app.workers",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=['app.workers.tasks']
)

celery_app.conf.update(
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    worker_max_tasks_per_child=1000,
    task_soft_time_limit=300,
    task_time_limit=600,
    broker_transport_options={
        "visibility_timeout": 3600,
        "max_retries": 3,
    },
    result_expires=86400,
)

celery_app.conf.beat_schedule = {
    'send-telegram-reminders-every-minute': {
        'task': 'app.workers.tasks.send_due_telegram_reminders',
        'schedule': 60.0
    },
}