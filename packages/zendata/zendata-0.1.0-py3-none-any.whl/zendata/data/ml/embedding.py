from pydantic import Field, BaseModel


class Embedding(BaseModel):
    vector: list[float] = Field(default_factory=list, description="Embedding vector")
