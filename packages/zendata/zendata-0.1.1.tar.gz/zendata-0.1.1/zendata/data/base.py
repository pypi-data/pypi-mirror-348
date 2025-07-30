from uuid import uuid4
from typing import Optional
from pydantic import BaseModel, Field
import time


class BaseData(BaseModel):
    id: str = Field(
        default_factory=lambda: uuid4().hex, description="ID unique de l’input"
    )
    type: str = Field(..., description="Type générique, ex: 'text', 'image', …")
    created_at: int = Field(
        default_factory=lambda: int(time.time()), description="Timestamp Unix"
    )
    extras: Optional[dict] = Field(None, description="Extras for any informations")
