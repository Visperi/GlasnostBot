from typing import TypedDict, NotRequired, List
from .message_entity import MessageEntity


class TextQuote(TypedDict):
    text: str
    entities: NotRequired[List[MessageEntity]]
    position: int
    is_manual: NotRequired[bool]
