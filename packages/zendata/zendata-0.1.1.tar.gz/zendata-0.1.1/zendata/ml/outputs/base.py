from uuid import uuid4
from pydantic import BaseModel, Field
from typing import Optional
import time


class BaseOutput(BaseModel):
    id: str = Field(
        default_factory=lambda: uuid4().hex, description="Unique id of output"
    )
    model_name: Optional[str]
    model_version: Optional[str]
    created_at: int = Field(default_factory=lambda: int(time.time()), ge=0)
    updated_at: Optional[int] = Field(default_factory=lambda: int(time.time()), ge=0)
