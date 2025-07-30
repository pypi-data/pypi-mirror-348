from zendata.data.base import BaseData


def test_instanciate_base_input():
    actual = BaseData(type="input")
    assert actual.id is not None
    assert isinstance(actual.created_at, int)
