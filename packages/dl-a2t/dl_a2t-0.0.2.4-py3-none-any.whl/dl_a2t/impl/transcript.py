from typing import TypedDict, cast

from ..utils.model import load_model


class Result(TypedDict):
    text: str
    segments: list[dict]


def transcribe_audio(file_path: str, model="tiny"):
    model = load_model(model)
    result = model.transcribe(file_path)
    return cast(Result, result)
