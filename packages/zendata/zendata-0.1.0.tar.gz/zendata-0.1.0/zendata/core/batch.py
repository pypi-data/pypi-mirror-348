from pydantic import Field
from typing import Generic, List, TypeVar
from zendata.data.base import BaseData

T = TypeVar("T")


class Batch(BaseData, Generic[T]):
    items: List[T] = Field(default_factory=list, description="List of item")
