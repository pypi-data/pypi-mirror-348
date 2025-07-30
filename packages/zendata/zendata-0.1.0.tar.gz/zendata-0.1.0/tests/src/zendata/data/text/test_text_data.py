from zendata.data.text.text import TextData


def test_text_data():
    actual = TextData(text="test")
    assert actual.id is not None
    assert isinstance(actual.created_at, int)
