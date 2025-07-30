from pydantic import Field
from zendata.data.ml.base import BaseMLData
from .segment import Segment


class SpeakerLevel(Segment):
    speaker_id: str = Field(..., description="Speaker id")


class PredicSpeakerLevel(SpeakerLevel):
    confidence: float = Field(..., description="Confidence of the word")


class GroundTruthDiarization(BaseMLData):
    diarizations: list[SpeakerLevel] = Field(
        default_factory=list, description="diarization level"
    )


class PredictedDiarization(BaseMLData):
    diarizations: list[PredicSpeakerLevel] = Field(
        default_factory=list, description="diarization level"
    )
