from zendata.ml.inputs.image import Image


def test_instanciate_image_input():
    actual = Image(
        width=23,
        height=23,
        source="test",
        filename="text.png",
        size=3,
        content_type="image/png",
        checksum="23",
    )
    assert actual.id is not None
    assert isinstance(actual.created_at, int)
    assert actual.type == "image"
