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


from typing_extensions import TypedDict, NotRequired


class DocumentBase(TypedDict):
    file_id: str
    file_unique_id: str
    file_size: NotRequired[int]


class PhotoSize(DocumentBase):
    width: int
    height: int


class Document(DocumentBase):
    thumb: NotRequired[PhotoSize]
    file_name: NotRequired[str]


class PlaybackDocument(Document):
    duration: int
    mime_type: NotRequired[str]


class Audio(PlaybackDocument):
    performer: NotRequired[str]
    title: NotRequired[str]


class Animation(PlaybackDocument):
    width: int
    height: int


class Video(PlaybackDocument):
    width: int
    height: int


class VideoNote(PlaybackDocument):
    length: int


class Voice(PlaybackDocument):
    pass


class MaskPosition(TypedDict):
    point: str
    x_shift: float
    y_shift: float
    scale: float


class Sticker(Document):
    type: str
    width: int
    height: int
    is_animated: bool
    is_video: bool
    emoji: NotRequired[str]
    set_name: NotRequired[str]
    premium_animation: NotRequired[Document]
    mask_position: NotRequired[MaskPosition]
    custom_emoji_id: NotRequired[str]
