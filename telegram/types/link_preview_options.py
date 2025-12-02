from typing import TypedDict, NotRequired


class LinkPreviewOptions(TypedDict):
    is_disabled: NotRequired[bool]
    url: NotRequired[str]
    prefer_small_media: NotRequired[bool]
    prefer_large_media: NotRequired[bool]
    show_above_text: NotRequired[bool]
