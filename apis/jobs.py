from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from database.dbSessionConfig import get_async_db
from sqlalchemy.ext.asyncio import AsyncSession
from models.jobs import Job

router = APIRouter()

class AddRequest(BaseModel):
    a:int
    b:int

@router.post("/jobs", status_code=202)
async def create_job(payload: AddRequest, session: AsyncSession = Depends(get_async_db)):
    job = Job(
        task_type="ADD_NUMBERS",
        payload={
            "num1": payload.a,
            "num2": payload.b,
        },
        status="QUEUED",
    )

    session.add(job)
    await session.commit()
    await session.refresh(job)

    return {
        "job_id": job.id,
        "status": job.status,
        "message": "Job submitted successfully"
    }


@router.get("/jobs/{job_id}", status_code=200)
async def get_job(job_id:str, session: AsyncSession = Depends(get_async_db)):
    job = await session.get(Job, job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    return {
        "job_id": job.id,
        "task_type": job.task_type,
        "payload": job.payload,
        "result": job.result,
        "status": job.status,
        "max_attempt": job.max_attempt,
    }