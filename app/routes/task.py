from fastapi import APIRouter

from app.schemas.task import EnqueueTaskRequest

router = APIRouter()


@router.post("/task")
async def create_task(task: EnqueueTaskRequest) -> dict[str, str]:
    """Enqueue a new task.

    Parameters
    ----------
    task : EnqueueTaskRequest
        The request body containing task details.

    Returns
    -------
    dict[str, str]
        A JSON response indicating task status and metadata.

    """
    return {"status": "queued", "type": task.type, "payload": task.payload.model_dump_json()}
