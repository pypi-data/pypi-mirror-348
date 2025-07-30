from pydantic import Field
from zendata.data.ml.base import BaseMLData


class QuestionAnswer(BaseMLData):
    question: str = Field(..., description="Question")
    answer: str = Field(..., description="Answer")
