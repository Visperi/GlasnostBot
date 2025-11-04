from typing import List

from typing_extensions import TypedDict, NotRequired

from .chat import Chat
from .user import User
from .message import Message


class Giveaway(TypedDict):
    chats: List[Chat]
    winners_selection_date: int
    winner_count: int
    only_new_members: NotRequired[bool]
    has_public_winners: NotRequired[bool]
    prize_description: NotRequired[str]
    country_codes: NotRequired[List[str]]
    prize_star_count: NotRequired[int]
    premium_subscription_month_count: NotRequired[int]


class GiveawayWinners(TypedDict):
    chat: Chat
    giveaway_message_id: int
    winners_selection_date: int
    winner_count: int
    winners: List[User]
    additional_chat_count: NotRequired[int]
    prize_star_count: NotRequired[int]
    premium_subscription_month_count: NotRequired[int]
    unclaimed_prize_count: NotRequired[int]
    only_new_members: NotRequired[bool]
    was_refunded: NotRequired[bool]
    prize_description: NotRequired[str]


class GiveawayCreated(TypedDict):
    prize_star_count: NotRequired[int]


class GiveawayCompleted(TypedDict):
    winner_count: int
    unclaimed_prize_count: NotRequired[int]
    giveaway_message: NotRequired[Message]
    is_star_giveaway: NotRequired[bool]
