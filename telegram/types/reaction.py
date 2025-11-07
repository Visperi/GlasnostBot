from typing import List

from typing_extensions import TypedDict, NotRequired

from .chat import Chat
from .user import User


class ReactionType(TypedDict):
    type: str


class ReactionTypeEmoji(ReactionType):
    emoji: str


class ReactionTypeCustomEmoji(ReactionType):
    custom_emoji_id: str


class ReactionTypePaid(ReactionType):
    pass


class ReactionCount(TypedDict):
    type: ReactionType
    total_count: int


# TODO: Move
class MessageReactionUpdated(TypedDict):
    chat: Chat
    message_id: int
    user: NotRequired[User]
    actor_chat: NotRequired[Chat]
    date: int
    old_reaction: List[ReactionType]
    new_reaction: List[ReactionType]


# TODO: Move
class MessageReactionCountUpdated(TypedDict):
    chat: Chat
    message_id: int
    date: int
    reactions: List[ReactionCount]
