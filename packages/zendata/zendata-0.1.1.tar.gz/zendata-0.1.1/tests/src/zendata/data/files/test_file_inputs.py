from zendata.data.files.file import File


def test_instanciate_file_input():
    actual = File(
        type="pdf",
        source="test",
        filename="text.pdf",
        size=3,
        content_type="application/pdf",
        checksum="23",
    )
    assert actual.id is not None
    assert isinstance(actual.created_at, int)
