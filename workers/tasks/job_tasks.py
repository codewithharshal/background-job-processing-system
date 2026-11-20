from workers.celery_app import celery_app
from services.job_service import process_job
from celery.exceptions import MaxRetriesExceededError


@celery_app.task(bind=True,name="jobs.process_job", max_retries=None)
def process_job_task(self, job_id:str):
    result = process_job(job_id)

    if result["status"] == "RETRY":
        attempt = result.get("attempt", 1)

        delay = min(5 * (2 ** (int(attempt) - 1)),300)

        raise self.retry(
            args=[job_id],
            countdown=delay,
            exc=RuntimeError(result.get("error", "Job failed"))
        )

    return result