from .types.link_preview_options import LinkPreviewOptions as LinkPreviewOptionsPayload


class LinkPreviewOptions:

    __slots__ = (
        "is_disabled",
        "url",
        "prefer_small_media",
        "prefer_large_media",
        "show_above_text"
    )

    def __init__(self, payload: LinkPreviewOptionsPayload):
        self.is_disabled = payload.get("is_disabled", False)
        self.url = payload.get("url")
        self.prefer_small_media = payload.get("prefer_small_media", False)
        self.prefer_large_media = payload.get("prefer_large_media", False)
        self.show_above_text = payload.get("show_above_text", False)
