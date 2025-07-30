from pydantic import Field
from zendata.data.ml.base import BaseMLData
from zendata.data.ml.classification import GTLabel, PredictLabel


class GtTextClassification(BaseMLData, GTLabel): ...


class TextClassification(BaseMLData, PredictLabel): ...
