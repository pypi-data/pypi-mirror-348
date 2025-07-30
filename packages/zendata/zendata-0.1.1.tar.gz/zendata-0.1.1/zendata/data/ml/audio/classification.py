from zendata.data.ml.base import BaseMLData
from zendata.data.ml.classification import GTLabel, PredictLabel


class GroundTruthClassificationAudio(BaseMLData, GTLabel): ...


class PredictedClassificationAudio(BaseMLData, PredictLabel): ...
