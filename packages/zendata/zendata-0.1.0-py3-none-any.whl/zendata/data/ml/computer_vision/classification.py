from pydantic import Field
from zendata.data.ml.base import BaseMLData
from zendata.data.ml.classification import GTLabel, PredictLabel


class GtImageClassification(BaseMLData, GTLabel): ...


class ImageClassification(BaseMLData, PredictLabel): ...
