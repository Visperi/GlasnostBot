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
