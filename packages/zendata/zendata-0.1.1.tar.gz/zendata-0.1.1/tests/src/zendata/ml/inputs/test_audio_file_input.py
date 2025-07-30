from zendata.ml.inputs.audio import Audio


def test_instanciate_audio_input():
    actual = Audio(
        frames=50000,
        channels=1,
        sample_rate=44000,
        source="test",
        filename="text.wav",
        size=3,
        content_type="audio/wav",
        checksum="23",
    )
    assert actual.id is not None
    assert isinstance(actual.created_at, int)
    assert actual.duration is not None
