from typing import Any, Optional
from pydantic import model_validator, Field
from .base import BaseTask


class Task(BaseTask):
    input_data: Any = Field(None, description="Data to process")
    output_data: Optional[Any] = Field(None, description="Result of processing")

    @model_validator(mode="after")
    def check_after_instantiation(self):
        """
        This runs *after* the instance is fully created.
        Raise here to reject bad input_data/output_data.
        """

        # 1) check input_data
        if self.input_data is not None:
            if self.input is not None and not isinstance(self.input_data, self.input):
                raise TypeError(f"{self.input_data!r} is not instance of {self.input}")

        # 2) check output_data if already set
        if self.output_data is not None:
            if self.output is not None and not isinstance(
                self.output_data, self.output
            ):
                raise TypeError(
                    f"{self.output_data!r} is not instance of {self.output}"
                )

        return self
