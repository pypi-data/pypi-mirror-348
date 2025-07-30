from __future__ import annotations
from typing import Optional, Literal
from pydantic import Field, model_validator
from zendata.data.base import BaseData


class Health(BaseData):
    type: str = "health"
    name: str = Field(..., description="Service name")
    dependencies: list[Health] = Field(default_factory=list, description="Dependencies")
    status_code: int = Field(default=200, description="Http satus code")
    status: Literal["healthy", "unhealthy"] = Field("healthy", description="Status")
    error: Optional[str] = Field(None, description="Error raised")

    @model_validator(mode="before")
    def calculate_health(cls, values):
        dependencies: list[Health] = values.get("dependencies", [])
        errors = values.get("error", None)

        for health in dependencies:
            if health.status != "healthy":
                values["status"] = "unhealthy"
                values["status_code"] = health.status_code
                if health.error:
                    if errors is None:
                        errors = ""
                    errors += f"service: {health.name} - error {health.error}" + "\n"
        values["error"] = errors
        return values
