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


from typing import List

from typing_extensions import TypedDict, NotRequired


class MediaBase(TypedDict):
    file_id: str
    file_unique_id: str
    file_size: NotRequired[int]


# TODO: Rename to e.g. DownloadableFile
class File(MediaBase):
    """
    A file ready to be downloaded. Type File in Telegram API.
    """
    file_path: NotRequired[str]


class PhotoSize(MediaBase):
    width: int
    height: int


class Document(MediaBase):
    thumbnail: NotRequired[PhotoSize]
    file_name: NotRequired[str]
    mime_type: NotRequired[str]


class PlaybackDocument(Document):
    duration: int


class Video(PlaybackDocument):
    width: int
    height: int
    cover: NotRequired[List[PhotoSize]]
    start_timestamp: NotRequired[int]


class Audio(PlaybackDocument):
    performer: NotRequired[str]
    title: NotRequired[str]


class Animation(PlaybackDocument):
    width: int
    height: int


class VideoNote(MediaBase):
    length: int
    duration: int
    thumbnail: NotRequired[PhotoSize]


class Voice(MediaBase):
    duration: int
    mime_type: str


class MaskPosition(TypedDict):
    point: str
    x_shift: float
    y_shift: float
    scale: float


class Sticker(MediaBase):
    type: str
    width: int
    height: int
    is_animated: bool
    is_video: bool
    thumbnail: NotRequired[PhotoSize]
    emoji: NotRequired[str]
    set_name: NotRequired[str]
    premium_animation: NotRequired[File]
    mask_position: NotRequired[MaskPosition]
    custom_emoji_id: NotRequired[str]
    needs_repainting: NotRequired[bool]


class StickerSet(TypedDict):
    name: str
    title: str
    sticker_type: str
    stickers: List[Sticker]
    thumbnail: NotRequired[PhotoSize]


class InputSticker(TypedDict):
    sticker: str
    format: str
    emoji_list: List[str]
    mask_position: NotRequired[MaskPosition]
    keywords: NotRequired[List[str]]


class PaidMedia(TypedDict):
    type: str


class PaidMediaPreview(PaidMedia):
    width: NotRequired[int]
    height: NotRequired[int]
    duration: NotRequired[int]


class PaidMediaPhoto(PaidMedia):
    photo: List[PhotoSize]


class PaidMediaVideo(PaidMedia):
    video: Video


class PaidMediaInfo(TypedDict):
    star_count: int
    paid_media: List[PaidMedia]
