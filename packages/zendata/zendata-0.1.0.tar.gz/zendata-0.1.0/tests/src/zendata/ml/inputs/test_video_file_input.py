from zendata.ml.inputs.video import Video


def test_instanciate_video_input():
    actual = Video(
        frames=50000,
        fps=60,
        height=200,
        width=200,
        source="test",
        filename="text.mp4",
        size=3,
        content_type="audio/mp4",
        checksum="23",
    )
    assert actual.id is not None
    assert isinstance(actual.created_at, int)
    assert actual.duration is not None
