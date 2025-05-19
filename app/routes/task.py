from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_task_queue
from app.errors.task_queue_error import TaskQueueError
from app.interfaces.task_queue import TaskQueue
from app.schemas.task import EnqueueTaskRequest

router = APIRouter()


@router.post("/task")
async def create_task(
    task: EnqueueTaskRequest,
    queue: TaskQueue = Depends(get_task_queue),  # noqa: B008
) -> dict[str, str]:
    """Enqueue a new task.

    Parameters
    ----------
    task : EnqueueTaskRequest
        The request body containing task details.
    queue : TaskQueue
        Injected task queue dependency.

    Returns
    -------
    dict[str, str]
        A JSON response indicating task status and metadata.

    """
    try:
        await queue.enqueue(task.model_dump())
        return {"status": "queued", "type": task.type, "payload": task.payload.model_dump_json()}
    except TaskQueueError as e:
        raise HTTPException(status_code=424, detail={"status": "error", "message": str(e)})
