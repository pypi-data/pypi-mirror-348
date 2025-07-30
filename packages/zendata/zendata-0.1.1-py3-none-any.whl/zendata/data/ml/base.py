from typing import Optional
from pydantic import Field
from zendata.data.base import BaseData


class BaseMLData(BaseData):
    source_id: Optional[str] = Field(None, description="Source id of the data")
    model_id: Optional[str] = Field(None, description="model id")
    version: Optional[str] = Field(None, description="Version id of the model")
