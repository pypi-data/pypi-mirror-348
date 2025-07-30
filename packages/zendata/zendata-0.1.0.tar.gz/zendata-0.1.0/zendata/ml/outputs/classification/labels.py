from pydantic import Field, BaseModel
from ..base import BaseOutput


class BaseLabel(BaseModel):
    label: str = Field(..., description="The predicted label")

    probability: float = Field(
        ..., ge=0.0, le=1.0, description="The predicted probability of the label"
    )


class Label(BaseOutput):
    label: BaseLabel = Field(
        ..., description="The predicted label with its probability"
    )


class MultiLabels(BaseOutput):
    labels: list[BaseLabel] = Field(
        ..., description="List of predicted labels with their probabilities"
    )
