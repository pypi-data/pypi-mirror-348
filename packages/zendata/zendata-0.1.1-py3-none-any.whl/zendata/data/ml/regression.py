from pydantic import Field
from zendata.data.base import BaseData


class RegressionOutput(BaseData):
    value: float = Field(..., description="Predicted value")
