from typing import Literal
from .base import BaseInput
from pydantic import Field


class TextInput(BaseInput):
    type: Literal["text"] = "text"
    text: str = Field(..., description="Raw text")
