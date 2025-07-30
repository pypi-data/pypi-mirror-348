from pydantic import Field
from zendata.data.ml.base import BaseMLData
from .segment import Segment


class WordLevel(Segment):
    word: str = Field(..., description="Word")


class PredictWordLevel(WordLevel):
    confidence: float = Field(..., description="Confidence of the word")


class GroundTruthTranscription(BaseMLData):
    transcriptions: list[WordLevel] = Field(
        default_factory=list, description="Transcription level"
    )


class PredictedTranscription(BaseMLData):
    transcriptions: list[PredictWordLevel] = Field(
        default_factory=list, description="Transcription level"
    )
