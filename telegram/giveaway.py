from .types.giveaway import (
    GiveawayBase as GiveawayBasePayload,
    Giveaway as GiveawayPayload,
    GiveawayWinners as GiveawayWinnersPayload,
    GiveawayCreated as GiveawayCreatedPayload,
    GiveawayCompleted as GiveawayCompletedPayload
)
from .chat import Chat
from .user import User
from .message import Message


class GiveawayBase:

    __slots__ = (
        "winners_selection_date",
        "winner_count",
        "only_new_members",
        "prize_description",
        "prize_star_count",
        "premium_subscription_month_count"
    )

    def __init__(self, payload: GiveawayBasePayload):
        self.winners_selection_date = payload["winners_selection_date"]
        self.winner_count = payload["winner_count"]
        self.only_new_members = payload.get("only_new_members", False)
        self.prize_description = payload.get("prize_description")
        self.prize_star_count = payload.get("prize_star_count", 0)
        self.premium_subscription_month_count = payload.get("premium_subscription_month_count", 0)


class Giveaway(GiveawayBase):

    __slots__ = (
        "chats",
        "has_public_winners",
        "country_codes"
    )

    def __init__(self, payload: GiveawayPayload):
        super().__init__(payload)
        self.chats = [Chat(c) for c in payload["chats"]]
        self.has_public_winners = payload.get("has_public_winners", False)
        self.country_codes = payload.get("country_codes", [])


class GiveawayWinners(GiveawayBase):

    __slots__ = (
        "chat",
        "giveaway_message_id",
        "winners",
        "additional_chat_count",
        "unclaimed_prize_count",
        "was_refunded"
    )

    def __init__(self, payload: GiveawayWinnersPayload):
        super().__init__(payload)
        self.chat = Chat(payload["chat"])
        self.giveaway_message_id = payload["giveaway_message_id"]
        self.winners = [User(u) for u in payload["winners"]]
        self.additional_chat_count = payload.get("additional_chat_count", 0)
        self.unclaimed_prize_count = payload.get("unclaimed_prize_count", 0)
        self.was_refunded = payload.get("was_refunded", False)


class GiveawayCreated:

    __slots__ = (
        "prize_star_count"
    )

    def __init__(self, payload: GiveawayCreatedPayload):
        self.prize_star_count = payload.get("prize_star_count", 0)


class GiveawayCompleted:

    __slots__ = (
        "winner_count",
        "unclaimed_prize_count",
        "giveaway_message",
        "is_star_giveaway"
    )

    def __init__(self, payload: GiveawayCompletedPayload):
        self.winner_count = payload["winner_count"]
        self.unclaimed_prize_count = payload.get("unclaimed_prize_count", 0)
        self.is_star_giveaway = payload.get("is_star_giveaway", False)

        try:
            self.giveaway_message = Message(payload["giveaway_message"])
        except KeyError:
            self.giveaway_message = None
