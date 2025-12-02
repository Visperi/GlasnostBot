from typing import TypedDict, NotRequired

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