from typing import Any
from pydantic import Field
from zendata.data.vectors.tensor import TensorInput


class ImageData(TensorInput):
    type: str = "image-data"
    data: list[Any] = Field(default_factory=list, description="Image data")
    width: int = Field(..., description="Width of the image in pixels")
    height: int = Field(..., description="Height of the image in pixels")


class ImageBytesData(ImageData):
    type: str = "image-bytes-data"
    data: bytes = Field(..., description="Image data in bytes")
