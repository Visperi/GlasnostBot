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


from .types.chat_boost import (
    ChatBoostSource as ChatBoostSourcePayload,
    ChatBoostSourcePremium as ChatBoostSourcePremiumPayload,
    ChatBoostSourceGiftCode as ChatBoostSourceGiftCodePayload,
    ChatBoostSourceGiveaway as ChatBoostSourceGiveawayPayload,
    ChatBoost as ChatBoostPayload,
    ChatBoostUpdated as ChatBoostUpdatedPayload,
    ChatBoostRemoved as ChatBoostRemovedPayload,
    ChatBoostAdded as ChatBoostAddedPayload
)
from .chat import Chat
from .user import User


class ChatBoostSource:

    __slots__ = (
        "source"
    )

    def __init__(self, payload: ChatBoostSourcePayload):
        self.source = payload["source"]


class ChatBoostSourcePremium(ChatBoostSource):

    __slots__ = (
        "user"
    )

    def __init__(self, payload: ChatBoostSourcePremiumPayload):
        super().__init__(payload)
        self.user = User(payload["user"])


class ChatBoostSourceGiftCode(ChatBoostSource):

    __slots__ = (
        "user"
    )

    def __init__(self, payload: ChatBoostSourceGiftCodePayload):
        super().__init__(payload)
        self.user = User(payload["user"])


class ChatBoostSourceGiveaway(ChatBoostSource):

    __slots__ = (
        "giveaway_message_id",
        "user",
        "prize_star_count",
        "is_unclaimed"
    )

    def __init__(self, payload: ChatBoostSourceGiveawayPayload):
        super().__init__(payload)
        self.giveaway_message_id = payload["giveaway_message_id"]
        self.prize_star_count = payload.get("prize_star_count", 0)
        self.is_unclaimed = payload.get("is_unclaimed", False)

        try:
            self.user = User(payload["user"])
        except KeyError:
            self.user = None

    @property
    def message_sent(self):
        return self.giveaway_message_id != 0


class ChatBoost:

    __slots__ = (
        "boost_id",
        "add_date",
        "expiration_date",
        "source"
    )

    def __init__(self, payload: ChatBoostPayload):
        self.boost_id = payload["boost_id"]
        self.add_date = payload["add_date"]
        self.expiration_date = payload["expiration_date"]
        self.source = ChatBoostSource(payload["source"])


class ChatBoostUpdated:

    __slots__ = (
        "chat",
        "boost"
    )

    def __init__(self, payload: ChatBoostUpdatedPayload):
        self.chat = Chat(payload["chat"])
        self.boost = ChatBoost(payload["boost"])


class ChatBoostRemoved:

    __slots__ = (
        "chat",
        "boost_id",
        "remove_date",
        "source"
    )

    def __init__(self, payload: ChatBoostRemovedPayload):
        self.chat = Chat(payload["chat"])
        self.boost_id = payload["boost_id"]
        self.remove_date = payload["remove_date"]
        self.source = ChatBoostSource(payload["source"])


class ChatBoostAdded:

    __slots__ =(
        "boost_count"
    )

    def __init__(self, payload: ChatBoostAddedPayload):
        self.boost_count = payload["boost_count"]
