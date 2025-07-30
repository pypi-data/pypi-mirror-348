from pydantic import Field, model_validator
from .file import File


class Video(File):
    type: str = "video"
    frames: int = Field(..., description="Number of frames in the video file")
    width: int = Field(..., description="Width of the video in pixels")
    height: int = Field(..., description="Height of the video in pixels")
    fps: float = Field(..., description="Frames per second of the video")
    duration: float = Field(
        ..., ge=0, description="Duration of the video file in seconds"
    )

    @model_validator(mode="before")
    def calculate_duration(cls, values):
        frames = values.get("frames")
        fps = values.get("fps")

        if frames is not None and fps is not None:
            # Calculer la durée en secondes : frames / fps
            values["duration"] = frames / fps

        return values
