from typing import List
from typing_extensions import TypedDict, NotRequired
from .document import PhotoSize, Animation
from .message import MessageEntity


class Dice(TypedDict):
    emoji: str
    value: int


class Game(TypedDict):
    title: str
    description: str
    photo: List[PhotoSize]
    text: NotRequired[str]
    text_entities: NotRequired[List[MessageEntity]]
    animation: Animation
