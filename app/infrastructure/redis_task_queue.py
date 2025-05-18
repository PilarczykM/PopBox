import inspect
import json

import redis

from app.errors.task_queue_error import TaskQueueError
from app.interfaces.task_queue import TaskQueue


class RedisTaskQueue(TaskQueue):
    """Redis implementation of TaskQueue."""

    def __init__(self, redis_url: str = "redis://redis:6379", default_queue: str = "default") -> None:
        self._redis = redis.from_url(redis_url, decode_responses=True)
        self._default_queue = default_queue

    async def enqueue(self, task: dict, queue_name: str | None = None) -> int:
        """Enqueue method.

        Parameters
        ----------
        task : dict
            The task
        queue_name : str | None, optional
            The queue name, by default None

        Raises
        ------
        TaskQueueError
            Raised when a task queue operation fails.

        """
        queue = queue_name or self._default_queue

        try:
            serialized = json.dumps(task)
            result = self._redis.rpush(queue, serialized)
            if inspect.isawaitable(result):
                return await result
            else:
                return result
        except redis.RedisError as e:
            msg = f"Failed to enqueue task to queue '{queue}': {e}"
            raise TaskQueueError(msg) from e
