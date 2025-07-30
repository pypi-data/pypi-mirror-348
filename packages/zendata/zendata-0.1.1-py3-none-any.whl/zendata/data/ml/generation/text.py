from typing import Any
from zendata.data.ml.base import BaseMLData
from zendata.data.base import BaseData


class Prompt(BaseMLData):
    type: str = "prompt"
    prompt: str


class Generation(BaseMLData):
    type: str = "generation"
    output_text: str


class Summary(Generation):
    type: str = "summary"


class Message(BaseData):
    type: str = "message"
    user_id: str
    message: str


class Conversation(BaseData):
    type: str = "conversation"
    conversation_id: str
    messages: list[Message]


class Text2Image(BaseMLData):
    type: str = "text-to-image"
    output_image: Any
