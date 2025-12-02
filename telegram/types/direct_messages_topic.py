from typing import TypedDict, NotRequired

from .user import User


class DirectMessagesTopic(TypedDict):
    topic_id: int
    user: NotRequired[User]
