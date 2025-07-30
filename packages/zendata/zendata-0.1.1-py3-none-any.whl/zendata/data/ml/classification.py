from pydantic import Field, BaseModel
from zendata.data.base import BaseData


class GTLabel(BaseModel):
    label: str = Field(..., description="Classification labels")


class PredictLabel(GTLabel):
    confidence: float = Field(0.0, ge=0, le=1.0, description="Confidence of label")


class GTMultiClassClassification(BaseData):
    label: GTLabel = Field(..., description="Classification labels and confidence")


class MultiClassClassification(BaseData):
    label: PredictLabel = Field(..., description="Classification labels and confidence")


class MultiLabelClassification(BaseModel):
    labels: list[PredictLabel] = Field(
        default_factory=list, description="Classifications labels and confidence"
    )
