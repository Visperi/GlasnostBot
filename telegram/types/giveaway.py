from typing import List

from typing_extensions import TypedDict, NotRequired

from .chat import Chat
from .user import User


class GiveawayBase(TypedDict):
    winners_selection_date: int
    winner_count: int
    only_new_members: NotRequired[bool]
    prize_description: NotRequired[str]
    prize_star_count: NotRequired[int]
    premium_subscription_month_count: NotRequired[int]


class Giveaway(GiveawayBase):
    chats: List[Chat]
    has_public_winners: NotRequired[bool]
    country_codes: NotRequired[List[str]]


class GiveawayWinners(GiveawayBase):
    chat: Chat
    giveaway_message_id: int
    winners: List[User]
    additional_chat_count: NotRequired[int]
    unclaimed_prize_count: NotRequired[int]
    was_refunded: NotRequired[bool]


class GiveawayCreated(TypedDict):
    prize_star_count: NotRequired[int]
