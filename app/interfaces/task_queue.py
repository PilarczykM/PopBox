from abc import ABC, abstractmethod


class TaskQueue(ABC):
    """Abstract base class representing an asynchronous task queue interface."""

    @abstractmethod
    async def enqueue(self, task: dict) -> None:
        """Asynchronously add a task to the queue.

        Parameters
        ----------
        task: dict
            A dictionary representing the task payload.

        """
        pass
