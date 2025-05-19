import os

from app.infrastructure.redis_task_queue import RedisTaskQueue
from app.interfaces.task_queue import TaskQueue


def get_task_queue() -> TaskQueue:
    """Dependency provider for the task queue.

    This function instantiates and returns a Redis-based implementation
    of the TaskQueue interface. It is intended to be used with FastAPI's
    dependency injection system (via `Depends on`) to decouple route logic
    from queue instantiation.

    Returns
    -------
    TaskQueue
        A Redis-backed task queue instance.

    """
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
    return RedisTaskQueue(redis_url=redis_url)
