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


from .utils import flatten_handlers
from .types.media import (
    MediaBase as MediaBasePayload,
    Document as DocumentPayload,
    PhotoSize as PhotoSizePayload,
    Audio as AudioPayload,
    Animation as AnimationPayload,
    Video as VideoPayload,
    VideoNote as VideoNotePayload,
    Voice as VoicePayload,
    MaskPosition as MaskPositionPayload,
    Sticker as StickerPayload,
    File as FilePayload,
    PlaybackDocument as PlaybackDocumentPayload,
    StickerSet as StickerSetPayload,
    InputSticker as InputStickerPayload,
    PaidMedia as PaidMediaPayload,
    PaidMediaPreview as PaidMediaPreviewPayload,
    PaidMediaPhoto as PaidMediaPhotoPayload,
    PaidMediaVideo as PaidMediaVideoPayload,
    PaidMediaInfo as PaidMediaInfoPayload
)


class MediaBase:

    __slots__ = (
        "file_id",
        "file_unique_id",
        "file_size"
    )

    def __init__(self, payload: MediaBasePayload):
        self.file_id = payload["file_id"]
        self.file_unique_id = payload["file_unique_id"]
        self.file_size = payload.get("file_size", -1)


class File(MediaBase):

    __slots__ = (
        "file_path"
    )

    def __init__(self, payload: FilePayload):
        super().__init__(payload)
        self.file_path = payload.get("file_path")


class PhotoSize(MediaBase):

    __slots__ = (
        "width",
        "height"
    )

    def __init__(self, payload: PhotoSizePayload):
        super().__init__(payload)
        self.width = payload["width"]
        self.height = payload["height"]


class Document(MediaBase):

    __slots__ = (
        "thumbnail",
        "file_name",
        "mime_type"
    )

    def __init__(self, payload: DocumentPayload):
        super().__init__(payload)
        self.file_name = payload.get("file_name")
        self.mime_type = payload.get("mime_type")

class PlaybackDocument(Document):

    __slots__ = (
        "duration"
    )

    def __init__(self, payload: PlaybackDocumentPayload):
        super().__init__(payload)
        self.duration = payload["duration"]


class Video(PlaybackDocument):

    __slots__ = (
        "width",
        "height",
        "cover",
        "start_timestamp"
    )

    def __init__(self, payload: VideoPayload):
        super().__init__(payload)
        self.width = payload["width"]
        self.height = payload["height"]
        self.cover = [PhotoSize(p) for p in payload.get("cover", [])]
        self.start_timestamp = payload.get("start_timestamp", 0)


class Audio(PlaybackDocument):

    __slots__ = (
        "performer",
        "title"
    )

    def __init__(self, payload: AudioPayload):
        super().__init__(payload)
        self.performer = payload.get("performer")
        self.title = payload.get("title")


class Animation(PlaybackDocument):

    __slots__ = (
        "width",
        "height"
    )

    def __init__(self, payload: AnimationPayload):
        super().__init__(payload)
        self.width = payload["width"]
        self.height = payload["height"]


class VideoNote(MediaBase):

    __slots__ = (
        "length",
        "duration",
        "thumbnail"
    )

    def __init__(self, payload: VideoNotePayload):
        super().__init__(payload)
        self.length = payload["length"]
        self.duration = payload["duration"]

        try:
            self.thumbnail = PhotoSize(payload["thumbnail"])
        except KeyError:
            self.thumbnail = None


class Voice(MediaBase):

    __slots__ = (
        "duration",
        "mime_type"
    )

    def __init__(self, payload: VoicePayload):
        super().__init__(payload)
        self.duration = payload["duration"]
        self.mime_type = payload["mime_type"]


class MaskPosition:

    __slots__ = (
        "point",
        "x_shift",
        "y_shift",
        "scale"
    )

    def __init__(self, payload: MaskPositionPayload):
        self.point = payload["point"]
        self.x_shift = payload["x_shift"]
        self.y_shift = payload["y_shift"]
        self.scale = payload["scale"]


class Sticker(MediaBase):
    _HANDLERS = []

    __slots__ = (
        "type",
        "width",
        "height",
        "is_animated",
        "is_video",
        "thumbnail",
        "emoji",
        "set_name",
        "premium_animation",
        "mask_position",
        "custom_emoji_id",
        "needs_repainting"
    )

    def __init__(self, payload: StickerPayload):
        super().__init__(payload)

        self.type = payload["type"]
        self.width = payload["width"]
        self.height = payload["height"]
        self.is_animated = payload["is_animated"]
        self.is_video = payload["is_video"]
        self.thumbnail = payload.get("thumbnail")
        self.emoji = payload.get("emoji")
        self.set_name = payload.get("set_name")
        self.premium_animation = payload.get("premium_animation")
        self.mask_position = payload.get("mask_position")
        self.custom_emoji_id = payload.get("custom_emoji_id")
        self.needs_repainting = payload.get("needs_repainting", False)

        for key, func in self._HANDLERS:
            try:
                value = payload[key]  # type: ignore
            except KeyError:
                continue
            else:
                func(self, value)

    def _handle_premium_animation(self, value):
        self.premium_animation = Document(value)

    def _handle_mask_position(self, value):
        self.mask_position = MaskPosition(value)

    def _handle_thumbnail(self, value):
        self.thumbnail = [PhotoSize(p) for p in value]


class StickerSet:

    __slots__ = (
        "name",
        "title",
        "sticker_type",
        "stickers",
        "thumbnail"
    )

    def __init__(self, payload: StickerSetPayload):
        self.name = payload["name"]
        self.title = payload["title"]
        self.sticker_type = payload["sticker_type"]
        self.stickers = [Sticker(s) for s in payload["stickers"]]

        try:
            self.thumbnail = payload["thumbnail"]
        except KeyError:
            self.thumbnail = None


@flatten_handlers
class InputSticker:
    _HANDLERS = []

    __slots__ = (
        "sticker",
        "format",
        "emoji_list",
        "mask_position",
        "keywords"
    )

    def __init__(self, payload: InputStickerPayload):
        self.sticker = payload["sticker"]
        self.format = payload["format"]
        self.emoji_list = payload["emoji_list"]
        self.keywords = payload.get("keywords")

        try:
            self.mask_position = MaskPosition(payload["mask_position"])
        except KeyError:
            self.mask_position = None


class PaidMedia:

    __slots__ = (
        "type"
    )

    def __init__(self, payload: PaidMediaPayload):
        self.type = payload["type"]


class PaidMediaPreview(PaidMedia):

    __slots__ = (
        "width",
        "height",
        "duration"
    )

    def __init__(self, payload: PaidMediaPreviewPayload):
        super().__init__(payload)
        self.width = payload.get("width")
        self.height = payload.get("height")
        self.duration = payload.get("duration")


class PaidMediaPhoto(PaidMedia):

    __slots__ = (
        "photo"
    )

    def __init__(self, payload: PaidMediaPhotoPayload):
        super().__init__(payload)
        self.photo = [PhotoSize(p) for p in payload["photo"]]


class PaidMediaVideo(PaidMedia):

    __slots__ = (
        "video"
    )

    def __init__(self, payload: PaidMediaVideoPayload):
        super().__init__(payload)
        self.video = Video(payload["video"])


class PaidMediaInfo:

    __slots__ = (
        "star_count",
        "paid_media"
    )

    def __init__(self, payload: PaidMediaInfoPayload):
        self.star_count = payload["star_count"]
        self.paid_media = [PaidMedia(p) for p in payload["paid_media"]]
