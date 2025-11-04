from typing_extensions import TypedDict, NotRequired

from .chat import Chat
from .user import User


# TODO: Combine/refactor the boost classes
class ChatBoostSource(TypedDict):
    source: str


class ChatBoostSourcePremium(ChatBoostSource):
    user: User


class ChatBoostSourceGiftCode(ChatBoostSource):
    user: User


class ChatBoostSourceGiveaway(ChatBoostSource):
    giveaway_message_id: int
    user: NotRequired[User]
    prize_star_count: NotRequired[int]
    is_unclaimed: NotRequired[bool]


class ChatBoost(TypedDict):
    boost_id: str
    add_date: int
    expiration_date: int
    source: ChatBoostSource


class ChatBoostRemoved(TypedDict):
    chat: Chat
    boost_id: str
    remove_date: int
    source: ChatBoostSource


class ChatBoostUpdated(TypedDict):
    chat: Chat
    boost: ChatBoost


class ChatBoostAdded(TypedDict):
    boost_count: int
