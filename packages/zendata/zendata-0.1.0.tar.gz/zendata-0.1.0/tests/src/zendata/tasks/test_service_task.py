import pytest
from unittest.mock import Mock
from typing import Any, Type

from zendata.tasks.service import Service, Task, TaskStatus, BaseTask


class DummyTask(BaseTask):
    input: Type[int] = int
    output: Type[str] = str


class DummyService(Service):
    def apply(self, task: Task, *args, **kwargs) -> Task:
        task.output_data = str(task.input_data * 2)
        return task


def test_run_successful_task():
    callback = Mock()
    service = DummyService(task_definition=DummyTask(), name="dummy", callback=callback)

    result_task = service.run(3, id="123")

    print(result_task.error)
    print(79 * "*")
    assert result_task.status == TaskStatus.COMPLETED.value
    assert result_task.input_data == 3
    assert result_task.output_data == "6"
    assert result_task.error is None
    assert result_task.id == "123"

    # Callback should have been called multiple times
    assert callback.call_count >= 3  # CREATED, STARTED, IN_PROGRESS, COMPLETED


def test_run_invalid_input_type():
    callback = Mock()
    service = DummyService(task_definition=DummyTask(), name="dummy", callback=callback)

    with pytest.raises(TypeError):
        service.run("not-an-int")


def test_run_invalid_output_type():
    class BadOutputService(Service):
        def apply(self, task: Task, *args, **kwargs):
            task.output_data = 123
            return task  # Not a string (expected output)

    callback = Mock()
    service = BadOutputService(
        task_definition=DummyTask(), name="bad_output", callback=callback
    )

    result_task = service.run(2)

    assert result_task.status == TaskStatus.FAILED.value
    assert "does not match expected output type" in result_task.error
    assert result_task.output_data is None


def test_run_apply_raises_exception():
    class ExplodingService(Service):
        def apply(self, task: Task, *args, **kwargs):
            raise RuntimeError("boom")

    callback = Mock()
    service = ExplodingService(
        task_definition=DummyTask(), name="explode", callback=callback
    )

    result_task = service.run(4)

    assert result_task.status == TaskStatus.FAILED.value
    assert "boom" in result_task.error
    assert result_task.output_data is None
