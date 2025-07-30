from pydantic import Field
from .file import File


class Image(File):
    type: str = "image"
    width: int = Field(..., description="Width of the image in pixels")
    height: int = Field(..., description="Height of the image in pixels")
