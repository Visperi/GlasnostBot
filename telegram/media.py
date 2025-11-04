"""
MIT License

Copyright (c) 2022 Niko Mätäsaho

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


from typing import Union
from .types.media import (
    MediaBase as DocumentBasePayload,
    Document as DocumentPayload,
    PhotoSize as PhotoSizePayload,
    PlaybackMediaBase as PlaybackDocumentPayload,
    Audio as AudioPayload,
    Animation as AnimationPayload,
    Video as VideoPayload,
    VideoNote as VideoNotePayload,
    Voice as VoicePayload,
    MaskPosition as MaskPositionPayload,
    Sticker as StickerPayload
)


class DocumentBase:

    __slots__ = (
        "file_id",
        "file_unique_id",
        "file_size"
    )

    def __init__(self, payload: DocumentBasePayload):
        self.file_id = payload["file_id"]
        self.file_unique_id = payload["file_unique_id"]
        self.file_size = payload.get("file_size", -1)


class PhotoSize(DocumentBase):

    __slots__ = (
        "width",
        "height"
    )

    def __init__(self, payload: PhotoSizePayload):
        super().__init__(payload)
        self._update(payload)

    def _update(self, payload: PhotoSizePayload):
        self.width = payload["width"]
        self.height = payload["height"]


class Document(DocumentBase):

    __slots__ = (
        "thumb",
        "file_name"
    )

    def __init__(self, payload: DocumentPayload):
        super().__init__(payload)
        self._update(payload)

    def _update(self, payload: DocumentPayload):
        self.file_name = payload.get("file_name")

        try:
            self.thumb = PhotoSize(payload["thumb"])
        except KeyError:
            self.thumb = None


class PlaybackDocument(Document):

    __slots__ = (
        "duration",
        "mime_type"
    )

    def __init__(self, payload: PlaybackDocumentPayload):
        super().__init__(payload)
        self._update(payload)

    def _update(self, payload: PlaybackDocumentPayload):
        self.duration = payload["duration"]
        self.mime_type = payload.get("mime_type")


class Audio(PlaybackDocument):

    __slots__ = (
        "performer",
        "title"
    )

    def __init__(self, payload: AudioPayload):
        super().__init__(payload)
        self._update(payload)

    def _update(self, payload: AudioPayload):
        self.performer = payload.get("performer")
        self.title = payload.get("title")


class VisualPlaybackDocument(PlaybackDocument):

    __slots__ = (
        "width",
        "height"
    )

    def __init__(self, payload: Union[AnimationPayload, VideoPayload]):
        super().__init__(payload)
        self.width = payload["width"]
        self.height = payload["height"]


class Animation(VisualPlaybackDocument):

    def __init__(self, payload: AnimationPayload):
        super().__init__(payload)


class Video(VisualPlaybackDocument):

    def __init__(self, payload: VideoPayload):
        super().__init__(payload)


class VideoNote(PlaybackDocument):

    __slots__ = "length"

    def __init__(self, payload: VideoNotePayload):
        super().__init__(payload)
        self.length = payload["length"]


class Voice(PlaybackDocument):

    def __init__(self, payload: VoicePayload):
        super().__init__(payload)


class MaskPosition:

    __slots__ = (
        "point",
        "x_shift",
        "y_shift",
        "scale"
    )

    def __init__(self, payload: MaskPositionPayload):
        self._update(payload)

    def _update(self, payload: MaskPositionPayload):
        self.point = payload["point"]
        self.x_shift = payload["x_shift"]
        self.y_shift = payload["y_shift"]
        self.scale = payload["scale"]


class Sticker(Document):

    __slots__ = (
        "type",
        "width",
        "height",
        "is_animated",
        "is_video",
        "emoji",
        "set_name",
        "premium_animation",
        "mask_position",
        "custom_emoji_id"
    )

    def __init__(self, payload: StickerPayload):
        super().__init__(payload)
        self._update(payload)

    def _update(self, payload: StickerPayload):
        self.type = payload["type"]
        self.width = payload["width"]
        self.height = payload["height"]
        self.is_animated = payload["is_animated"]
        self.is_video = payload["is_video"]
        self.emoji = payload.get("emoji")
        self.set_name = payload.get("set_name")
        self.premium_animation = payload.get("premium_animation")
        self.mask_position = payload.get("mask_position")
        self.custom_emoji_id = payload.get("custom_emoji_id")

        for slot in ("premium_animation", "mask_position"):
            try:
                getattr(self, f"_handle_{slot}")(payload[slot])  # type: ignore
            except KeyError:
                continue

    def _handle_premium_animation(self, value):
        self.premium_animation = Document(value)

    def _handle_mask_position(self, value):
        self.mask_position = MaskPosition(value)
