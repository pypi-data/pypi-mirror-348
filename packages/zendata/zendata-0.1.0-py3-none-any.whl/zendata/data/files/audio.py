from pydantic import Field, model_validator
from .file import File


class Audio(File):
    type: str = "audio"
    frames: int = Field(..., description="Number of frames in the audio file")
    channels: int = Field(
        ..., description="Number of audio channels (e.g., 1 for mono, 2 for stereo)"
    )
    sample_rate: int = Field(
        ..., description="Sampling rate of the audio file (e.g., 44100 Hz)"
    )
    duration: float = Field(
        ..., ge=0, description="Duration of the audio file in seconds"
    )

    @model_validator(mode="before")
    def calculate_duration(cls, values):
        frames = values.get("frames")
        sample_rate = values.get("sample_rate")

        if frames is not None and sample_rate is not None:
            values["duration"] = frames / sample_rate

        return values
