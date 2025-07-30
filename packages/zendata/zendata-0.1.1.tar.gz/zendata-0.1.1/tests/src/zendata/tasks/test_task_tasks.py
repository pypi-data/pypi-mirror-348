import pytest
from zendata.tasks.task import Task
from zendata.tasks.base import BaseTask


def test_task_valid_input_output():
    task = Task(
        name="test-task", input=str, output=int, input_data="hello", output_data=42
    )

    assert task.input_data == "hello"
    assert task.output_data == 42
    assert task.input == str
    assert task.output == int


def test_task_invalid_input_type():
    with pytest.raises(TypeError) as exc_info:
        Task(name="bad-input", input=int, output=str, input_data="not-an-int")
    assert "not-an-int" in str(exc_info.value)
    assert "is not instance of" in str(exc_info.value)


def test_task_invalid_output_type():
    with pytest.raises(TypeError) as exc_info:
        Task(
            name="bad-output", input=str, output=dict, input_data="ok", output_data=123
        )
    assert "123" in str(exc_info.value)
    assert "is not instance of" in str(exc_info.value)


def test_task_with_none_data():
    # Should not raise error if input_data and output_data are None
    task = Task(
        name="nullable", input=str, output=int, input_data=None, output_data=None
    )
    assert task.input_data is None
    assert task.output_data is None
