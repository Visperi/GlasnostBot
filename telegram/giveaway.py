"""
MIT License

Copyright (c) 2025 Niko Mätäsaho

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


from .types.giveaway import (
    GiveawayBase as GiveawayBasePayload,
    Giveaway as GiveawayPayload,
    GiveawayWinners as GiveawayWinnersPayload,
    GiveawayCreated as GiveawayCreatedPayload
)
from .chat import Chat
from .user import User


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
