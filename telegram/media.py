"""
MIT License

Copyright (c) 2025 Niko Mätäsaho

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
    """
    A base class for file objects sent to Telegram.

    Attributes:
        file_id: Identifier to the file. Can be used to download or reuse the file.
        file_unique_id: Unique identifier for the file. Supposed to be same over time. Cant be used to download or
                        reuse the file.
        file_size: File size in bytes.
    """

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
    """
    Represents a file ready to be downloaded. It is guaranteed that the File is downloadable for at least an hour
    before it should be requested again from Telegram API by its file ID.

    Attributes:
        file_path: Path at the Telegram API to download the file.
    """

    __slots__ = (
        "file_path"
    )

    def __init__(self, payload: FilePayload):
        super().__init__(payload)
        self.file_path = payload.get("file_path")


class PhotoSize(MediaBase):
    """
    Represents a single photo or thumbnail.

    Attributes:
        width: The photo width in pixels.
        height: The photo height in pixels.
    """

    __slots__ = (
        "width",
        "height"
    )

    def __init__(self, payload: PhotoSizePayload):
        super().__init__(payload)
        self.width = payload["width"]
        self.height = payload["height"]


class Document(MediaBase):
    """
    Represents a generic file in Telegram API.

    Attributes:
        thumbnail: Thumbnail for the file, if defined by the sender.
        file_name: Original filename for the file, defined by the sender.
        mime_type: MIME type of the file, defined by the sender.
    """

    __slots__ = (
        "thumbnail",
        "file_name",
        "mime_type"
    )

    def __init__(self, payload: DocumentPayload):
        super().__init__(payload)
        self.file_name = payload.get("file_name")
        self.mime_type = payload.get("mime_type")

        try:
            self.thumbnail = PhotoSize(payload["thumbnail"])
        except KeyError:
            self.thumbnail = None

class PlaybackDocument(Document):
    """
    A base class for files that are not static and can be played.

    Attributes:
        duration: Duration of the file in seconds.
    """

    __slots__ = (
        "duration"
    )

    def __init__(self, payload: PlaybackDocumentPayload):
        super().__init__(payload)
        self.duration = payload["duration"]


class Video(PlaybackDocument):
    """
    Represents a video file.

    Attributes:
        width: Width of the video in pixels.
        height: Height of the video in pixels.
        cover: The video cover art in a list of different size photos.
        start_timestamp: Timestamp in seconds where the video is started at in Telegram chat.
    """

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
    """
    Represents an audio file treated as music in Telegram.

    Attributes:
        performer: Performer of the file. Can be set by the sender or by audio tags.
        title: Title of the file. Can se set by the sender or by audio tags.
    """

    __slots__ = (
        "performer",
        "title"
    )

    def __init__(self, payload: AudioPayload):
        super().__init__(payload)
        self.performer = payload.get("performer")
        self.title = payload.get("title")


class Animation(PlaybackDocument):
    """
    Represents an animated file, that is GIF or H.264/MPEG-4 AVC video without sound.

    Attributes:
        width: Width of the file in pixels.
        height: Height of the file in pixels.
    """

    __slots__ = (
        "width",
        "height"
    )

    def __init__(self, payload: AnimationPayload):
        super().__init__(payload)
        self.width = payload["width"]
        self.height = payload["height"]


class VideoNote(MediaBase):
    """
    Represents a video message.

    Attributes:
        length: Diameter of the video in pixels.
        duration: Duration of the video in seconds.
        thumbnail: The video thumbnail, if defined by the sender.
    """

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
    """
    Represents a voice message.

    Attributes:
        duration: Duration of the audio in seconds.
        mime_type: MIME type of the file, if defined by the sender.
    """

    __slots__ = (
        "duration",
        "mime_type"
    )

    def __init__(self, payload: VoicePayload):
        super().__init__(payload)
        self.duration = payload["duration"]
        self.mime_type = payload["mime_type"]


class MaskPosition:
    """
    Describes a position for a mask where it should be placed on faces by default.

    Attributes:
        point: Part of a face relative to which the mask should be placed. Can be "forehead", "eyes", "mouth" or "chin".
        x_shift: Shift by X-axis measured in widths of the mask scaled to the face size, from left to right.
                 For example, choosing -1.0 will place mask just to the left of the default mask position.
        y_shift: Shift by Y-axis measured in heights of the mask scaled to the face size, from top to bottom.
                 For example, 1.0 will place the mask just below the default mask position.
        scale: Mask scaling coefficient. For example, 2.0 doubles the size.
    """

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


@flatten_handlers
class Sticker(MediaBase):
    """
    Represents a sticker.

    Attributes:
        type: Type of the sticker. Can be "regular", "mask" or "custom_emoji". Independent of the sticker format.
        width: Width of the sticker in pixels.
        height: Height of the sticker in pixels.
        is_animated: True, if the sticker is animated.
        is_video: True, if the sticker is a video sticker.
        thumbnail: Thumbnail if the sticker is in WEBP or JPG format.
        emoji: Emoji associated with the sticker.
        set_name: Name of the sticker set the sticker belongs to.
        premium_animation: Premium animation for premium regular stickers.
        mask_position: Placement if a mask for mask stickers.
        custom_emoji_id: Unique identifier for custom emoji stickers.
        needs_repainting: True if the sticker must be repainted in messages. If True, the sticker is repainted to a
                          text color in messages, the color of the Telegram Premium badge in emoji status, white color
                          on chat photos, or another appropriate color in other places.
    """
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
    """
    Represents a sticker set.

    Attributes:
        name: Name of the sticker set.
        title: Title of the sticker set.
        sticker_type: Type of the stickers in the sticker set. Can be "regular", "mask" or "custom_emoji".
        stickers: List of ``telegram.Sticker`` in the sticker set.
        thumbnail: Thumbnail for the sticker set if set. Ca be in format WEBP, TGS or WEBM.
    """

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


class InputSticker:
    """
    Represents a sticker to be added to a sticker set.

    Attributes:
        sticker: The sticker object. Can be a file ID if the sticker already exists in Telegram servers, or an HTTP URL
                 to get the file from internet. Animated stickers and video stickers cannot be added via URLs.
        format: File format of the sticker. Must be "static" for WEBP and PNG files, "animated" for TGS files or
                "video" for WEBM files.
        emoji_list: List of 1-20 emojis associated with the sticker.
        mask_position: ``telegram.MaskPosition`` object describing the position where a mask should be placed on faces.
                       For "mask" stickers only.
        keywords: List of 0-20 search keywords for the sticker with total length up to 64 characters. For "regular" and
                  "custom_emoji" stickers only.
    """
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
    """
    A base class for paid media in a message. Paid media can be accessed by paying Telegram stars.

    Attributes:
        type: Type of the paid media. Can be "preview", "photo" or "video".
    """

    __slots__ = (
        "type"
    )

    def __init__(self, payload: PaidMediaPayload):
        self.type = payload["type"]


class PaidMediaPreview(PaidMedia):
    """
    A preview or a paid media that cannot be accessed before payment.

    Attributes:
        width: Media width in pixels.
        height: Media height in pixels.
        duration: Duration of the media in seconds, if it is a playable file.
    """

    __slots__ = (
        "width",
        "height",
        "duration"
    )

    def __init__(self, payload: PaidMediaPreviewPayload):
        super().__init__(payload)
        self.width = payload.get("width")
        self.height = payload.get("height")
        self.duration = payload.get("duration", 0)


class PaidMediaPhoto(PaidMedia):
    """
    A paid media that is a photo.

    Attributes:
        photo: List of the photo in different sizes.
    """

    __slots__ = (
        "photo"
    )

    def __init__(self, payload: PaidMediaPhotoPayload):
        super().__init__(payload)
        self.photo = [PhotoSize(p) for p in payload["photo"]]


class PaidMediaVideo(PaidMedia):
    """
    A paid media that is a video file.

    Attributes:
        video: The video file.
    """

    __slots__ = (
        "video"
    )

    def __init__(self, payload: PaidMediaVideoPayload):
        super().__init__(payload)
        self.video = Video(payload["video"])


class PaidMediaInfo:
    """
    Describes a paid media added to a message.

    Attributes:
        star_count: Number of Telegram stars that must be paid to get access to the media.
        paid_media: List of the media that can be accessed by the payment.
    """

    __slots__ = (
        "star_count",
        "paid_media"
    )

    def __init__(self, payload: PaidMediaInfoPayload):
        self.star_count = payload["star_count"]
        self.paid_media = [PaidMedia(p) for p in payload["paid_media"]]
