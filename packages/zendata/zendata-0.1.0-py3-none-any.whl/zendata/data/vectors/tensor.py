from typing import List, Optional
from pydantic import Field
from zendata.data.base import BaseData


class TensorInput(BaseData):
    data: list = Field(default_factory=list, description="Array of any type")
    shape: Optional[List[int]] = Field(None, description="Shape of your array")
    source_id: Optional[str] = Field(None, description="If any source is available")
