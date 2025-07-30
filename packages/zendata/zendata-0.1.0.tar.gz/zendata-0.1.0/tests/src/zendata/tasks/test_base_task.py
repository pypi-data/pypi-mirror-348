import pytest
from pydantic import ValidationError
from zendata.tasks.base import BaseTask, TaskStatus, deserialize_type


def test_base_task_creation():
    task = BaseTask(
        name="Test Task",
        status=TaskStatus.STARTED,
        percentage=0.5,
        input=str,
        output=dict,
    )
    assert task.name == "Test Task"
    assert task.status == TaskStatus.STARTED
    assert 0.0 <= task.percentage <= 1.0
    assert task.input is str
    assert task.output is dict
    assert task.error is None
    assert isinstance(task.id, str)
    assert isinstance(task.created_at, int)
    assert isinstance(task.updated_at, int)
    assert task.extras == {}


def test_percentage_bounds():
    with pytest.raises(ValidationError):
        BaseTask(percentage=-0.1)
    with pytest.raises(ValidationError):
        BaseTask(percentage=1.1)


def test_input_output_type_validation():
    # input/output must be a type or None
    with pytest.raises(ValidationError):
        BaseTask(name="test", input="not_a_type", output=str)
    with pytest.raises(TypeError):
        BaseTask(name="test", intput=str, output=123)


def test_updated_at_is_set_and_refreshed():
    task1 = BaseTask(name="test", input=str, output=str)
    old_updated = task1.updated_at

    # simulate a small delay then re-validate
    import time

    time.sleep(1)
    task2 = BaseTask.model_validate(task1.model_dump())
    assert task2.updated_at > old_updated


def test_serialization_of_input_output():
    task = BaseTask(input=str, output=dict)
    dumped = task.model_dump()
    assert dumped["input"] == "builtins.str"
    assert dumped["output"] == "builtins.dict"


def test_error_field():
    task = BaseTask(error="Something went wrong")
    assert task.error == "Something went wrong"


# Define a dummy class in this test module for testing
class DummyClass:
    pass


def test_deserialize_builtin_type():
    # Test that built-in types can be deserialized
    t = deserialize_type("builtins.str")
    assert t is str
    t = deserialize_type("builtins.int")
    assert t is int


def test_deserialize_standard_library_type():
    # Test a standard library class (datetime.datetime)
    t = deserialize_type("datetime.datetime")
    import datetime

    assert t is datetime.datetime


def test_deserialize_custom_class_in_test_module():
    # Use __name__ to reference this test module
    module_path = __name__
    class_name = "DummyClass"
    path = f"{module_path}.{class_name}"
    t = deserialize_type(path)
    assert t is DummyClass


def test_empty_path_returns_none():
    # Passing an empty string should return None
    assert deserialize_type("") is None
    assert deserialize_type(None) is None  # type: ignore


def test_invalid_module_raises_import_error():
    with pytest.raises(ImportError) as excinfo:
        deserialize_type("nonexistent_module.Class")
    assert "Cannot import name" in str(excinfo.value) or "No module named" in str(
        excinfo.value
    )


def test_invalid_class_in_valid_module_raises_import_error():
    # Valid module but class does not exist
    module_path = "builtins"
    with pytest.raises(ImportError) as excinfo:
        deserialize_type(f"{module_path}.NonExistentClass")
    assert "Cannot import name NonExistentClass from module builtins" in str(
        excinfo.value
    )


def test_set_status():
    task = BaseTask(
        name="Test Task",
        status=TaskStatus.STARTED,
        percentage=0.5,
        input=str,
        output=dict,
    )
    actual_updated_at = task.updated_at
    task.set_status(status=TaskStatus.COMPLETED.value)
    assert actual_updated_at <= task.updated_at
    assert task.status == TaskStatus.COMPLETED.value


def test_set_status_to_created():
    task = BaseTask(
        name="Test Task",
        status=TaskStatus.STARTED,
        percentage=0.5,
        input=str,
        output=dict,
    )
    actual_updated_at = task.updated_at
    task.set_status_to_created()
    assert actual_updated_at <= task.updated_at
    assert task.status == TaskStatus.CREATED.value


def test_set_status_to_started():
    task = BaseTask(
        name="Test Task",
        status=TaskStatus.STARTED,
        percentage=0.5,
        input=str,
        output=dict,
    )
    actual_updated_at = task.updated_at
    task.set_status_to_started()
    assert actual_updated_at <= task.updated_at
    assert task.status == TaskStatus.STARTED.value


def test_set_status_to_in_progress():
    task = BaseTask(
        name="Test Task",
        status=TaskStatus.STARTED,
        percentage=0.5,
        input=str,
        output=dict,
    )
    actual_updated_at = task.updated_at
    task.set_status_to_in_progress()
    assert actual_updated_at <= task.updated_at
    assert task.status == TaskStatus.IN_PROGRESS.value


def test_set_status_to_completed():
    task = BaseTask(
        name="Test Task",
        status=TaskStatus.STARTED,
        percentage=0.5,
        input=str,
        output=dict,
    )
    actual_updated_at = task.updated_at
    task.set_status_to_completed()
    assert actual_updated_at <= task.updated_at
    assert task.status == TaskStatus.COMPLETED.value


def test_set_status_to_failed():
    task = BaseTask(
        name="Test Task",
        status=TaskStatus.STARTED,
        percentage=0.5,
        input=str,
        output=dict,
    )
    actual_updated_at = task.updated_at
    task.set_status_to_failed(error="test")
    assert actual_updated_at <= task.updated_at
    assert task.status == TaskStatus.FAILED.value
    assert task.error == "test"


def test_set_status_to_retrying():
    task = BaseTask(
        name="Test Task",
        status=TaskStatus.STARTED,
        percentage=0.5,
        input=str,
        output=dict,
    )
    actual_updated_at = task.updated_at
    task.set_status_to_retrying()
    assert actual_updated_at <= task.updated_at
    assert task.status == TaskStatus.RETRYING.value


def test_set_status_to_canceled():
    task = BaseTask(
        name="Test Task",
        status=TaskStatus.STARTED,
        percentage=0.5,
        input=str,
        output=dict,
    )
    actual_updated_at = task.updated_at
    task.set_status_to_canceled(error="test")
    assert actual_updated_at <= task.updated_at
    assert task.status == TaskStatus.CANCELED.value
    assert task.error == "test"


def test_set_status_to_timeout():
    task = BaseTask(
        name="Test Task",
        status=TaskStatus.STARTED,
        percentage=0.5,
        input=str,
        output=dict,
    )
    actual_updated_at = task.updated_at
    task.set_status_to_timeout(error="test")
    assert actual_updated_at <= task.updated_at
    assert task.status == TaskStatus.TIMEOUT.value
    assert task.error == "test"
