from typing import Any, Callable
from abc import ABC, abstractmethod
from .base import BaseTask, TaskStatus
from .task import Task


class Service(ABC):
    """
    Base service that enforces:
      - `input` and `output` class attributes must be set to a type
      - the `apply` method’s signature matches those types
      - runtime checks of input/output in `run`
    """

    def __init__(
        self,
        task_definition: BaseTask,
        name: str,
        callback: Callable[[Task], None] = lambda task: print(
            task.id, task.status, task.created_at, task.updated_at
        ),
    ):
        self.task_definition = task_definition
        self.__name = name
        self._callback = callback

    def callback(self, task: Task, *args, **kwargs):
        try:
            self._callback(task)
        except Exception as e:
            print(f"CallBack Failed {e}")

    @property
    def name(self) -> str:
        return self.__name

    @abstractmethod
    def apply(self, task: Task, *args, **kwargs) -> Task:
        """Process the input_data and return the result."""
        ...

    def run(self, input_data: Any, *args, **kwargs) -> Task:
        """
        1. Validates that self.input_data is correct type
        2. Calls apply(...)
        3. Validates that the returned output matches self.output
           and stores it in self.output_data
        """
        task = Task(
            name=self.name,
            status=TaskStatus.CREATED.value,
            input=self.task_definition.input,
            input_data=input_data,
            output=self.task_definition.output,
        )
        task.set_status_to_started()
        if kwargs.get("id"):
            task.id = kwargs.get("id")
        self.callback(task=task)

        try:
            task.set_status_to_in_progress()
            self.callback(task=task)
            task = self.apply(task=task, *args, **kwargs)
        except Exception as e:
            task.set_status_to_failed(error=str(e))
            self.callback(task=task)
            return task

        if self.task_definition.output is not None and not isinstance(
            task.output_data, self.task_definition.output
        ):
            message = (
                f"{task.output_data!r} (type {type(task.output_data)}) does not match "
                f"expected output type {self.task_definition.output}"
            )
            task.output_data = None
            task.set_status_to_failed(error=message)
            self.callback(task=task)
            return task

        task.set_status_to_completed()
        self.callback(task=task)
        return task
