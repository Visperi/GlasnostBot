from typing_extensions import TypedDict


class WebAppData(TypedDict):
    data: str
    button_text: str


class WebAppInfo(TypedDict):
    url: str
