from zendata.ml.outputs.base import BaseOutput


def test_ml_base_output_instanciate():
    actual = BaseOutput(model_name="", model_version="")
    assert actual.model_name is not None
