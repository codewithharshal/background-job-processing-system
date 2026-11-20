from workers.celery_app import celery_app
from services.job_service import process_job

@celery_app.task(name="jobs.process_job")
def process_job_task(job_id:str):
    return process_job(job_id)