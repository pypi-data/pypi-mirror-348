from zendata.ml.inputs.base import BaseInput


def test_instanciate_base_input():
    actual = BaseInput(type="input")
    assert actual.id is not None
    assert isinstance(actual.created_at, int)
