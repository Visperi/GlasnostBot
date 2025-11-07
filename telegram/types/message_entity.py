from typing import List

from typing_extensions import TypedDict, NotRequired

from .user import User
from .chat import Chat


# TODO: Combine/refactor the message origin classes
class MessageOrigin(TypedDict):
    type: str
    date: int


class MessageOriginUser(MessageOrigin):
    sender_user: User


class MessageOriginHiddenUser(MessageOrigin):
    sender_user_name: str


class MessageOriginChat(MessageOrigin):
    sender_chat: Chat
    author_signature: NotRequired[str]


class MessageOriginChannel(MessageOrigin):
    chat: Chat
    message_id: int
    author_signature: NotRequired[str]


class DirectMessagesTopic(TypedDict):
    topic_id: int
    user: NotRequired[User]


# TODO: Move
class LinkPreviewOptions(TypedDict):
    is_disabled: NotRequired[bool]
    url: NotRequired[str]
    prefer_small_media: NotRequired[bool]
    prefer_large_media: NotRequired[bool]
    show_above_text: NotRequired[bool]


class MessageEntity(TypedDict):
    type: str
    offset: int
    length: int
    url: NotRequired[str]
    user: NotRequired[User]
    language: NotRequired[str]
    custom_emoji_id: NotRequired[str]


# TODO: Move
class TextQuote(TypedDict):
    text: str
    entities: NotRequired[List[MessageEntity]]
    position: int
    is_manual: NotRequired[bool]
