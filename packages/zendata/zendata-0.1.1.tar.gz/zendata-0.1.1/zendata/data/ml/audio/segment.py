from pydantic import Field, BaseModel


class Segment(BaseModel):
    start: float = Field(..., description="Start audio segement")
    end: float = Field(..., description="End audio segement")
