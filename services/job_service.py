from database.syncdbConfig import SessionLocal
from models.job_attempts import JobAttempt
from models.jobs import Job
from sqlalchemy import select, func
from services.task_handlers import TASK_HANDLERS

def process_job(job_id:str):
    with SessionLocal() as session:
        # 1 get job
        job = session.get(Job, job_id)

        # 2 check we have it or not
        if not job:
            return {"status":"Job NotFound"}

        if job.status in ("COMPLETED", "FAILED"):
            return {"status":job.status}

        # 3 check attempts
        attempt_count = session.scalar(select(func.count()).select_from(JobAttempt).where(JobAttempt.job_id == job_id)) or 0

        if attempt_count >= job.max_attempt:
            job.status = "FAILED"
            session.commit()

            return {"status":"FAILED", "reason":"Max attempts reached"}

        # 4 create new attempt
        attempt = JobAttempt(
            job_id=job.id,
            attempt=attempt_count + 1,
            status="PROCESSING"
        )

        job.status = "PROCESSING"
        session.add(attempt)
        session.commit()

        task_type = job.task_type
        payload = job.payload
        attempt_id = attempt.id

    # 5 exe actual task outsize the transcation
    try:
        handler = TASK_HANDLERS.get(task_type)

        if not handler:
            raise ValueError(f"Unknown task type: {task_type}")

        result = handler(payload or {})

        # 6 update task
        with SessionLocal() as session:
            job = session.get(Job, job_id)
            attempt = session.get(JobAttempt, attempt_id)

            if job is None:
                raise ValueError("Job not found")
            
            if attempt is None:
                raise ValueError("did not found any attempt")

            attempt.status = "COMPLETED"
            job.status = "COMPLETED"
            job.result = result

            session.commit()

        return {
            "status":"COMPLETED",
            "result":result
        }

    except Exception as exc:
        # 7 update on failure

        with SessionLocal() as session:
            job = session.get(Job, job_id)
            attempt = session.get(JobAttempt, attempt_id)

            if job is None:
                raise ValueError("Job not found")
            
            if attempt is None:
                raise ValueError("did not found any attempt")

            attempt.status = "FAILED"
            attempt.error_message = str(exc)

            if attempt.attempt >= job.max_attempt:
                job.status = "FAILED"
            else:
                job.status = "RETRY"

            session.commit()

        return {
            "status":job.status,
            "error":str(exc)
        }
