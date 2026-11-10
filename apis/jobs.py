from fastapi import APIRouter
from pydantic import BaseModel

from workers.tasks.csv_import import add_two_num

router = APIRouter()

class AddRequest(BaseModel):
    a:int
    b:int

@router.post("/jobs", status_code=202)
async def create_job(payload: AddRequest):
    task = add_two_num.delay(payload.a,payload.b)

    return {
        "task_id":task.id,
        "status":"queued",
    }
    