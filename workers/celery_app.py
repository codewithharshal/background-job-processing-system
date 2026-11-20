import os

from celery import Celery

broker_url = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
result_backend = os.getenv("CELERY_RESULT_BACKEND")

celery_app = Celery(
    "background_jobs",
    broker=broker_url,
    backend=result_backend,
    include=["workers.tasks.job_tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    task_ignore_result=True,
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    task_soft_time_limit=840,
    task_time_limit=900,
    broker_connection_retry_on_startup=True,
)
