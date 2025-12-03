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

from datetime import datetime, UTC

from .chat import Chat
from .media import Sticker
from .message_entity import MessageEntity
from .types.gift import (
    GiftBase as GiftBasePayload,
    Gift as GiftPayload,
    UniqueGiftModelBase as UniqueGiftModelBasePayload,
    UniqueGiftModel as UniqueGiftModelPayload,
    UniqueGiftSymbol as UniqueGiftSymbolPayload,
    UniqueGiftBackdropColors as UniqueGiftBackdropColorsPayload,
    UniqueGiftBackdrop as UniqueGiftBackdropPayload,
    UniqueGift as UniqueGiftPayload,
    GiftInfoBase as GiftInfoBasePayload,
    GiftInfo as GiftInfoPayload,
    UniqueGiftInfo as UniqueGiftInfoPayload
)


class GiftBase:

    __slots__ = (
        "publisher_chat"
    )

    def __init__(self, payload: GiftBasePayload):
        try:
            self.publisher_chat = Chat(payload["publisher_chat"])
        except KeyError:
            self.publisher_chat = None


class Gift(GiftBase):

    __slots__ = (
        "id",
        "sticker",
        "star_count",
        "upgrade_star_count",
        "total_count",
        "remaining_count"
    )

    def __init__(self, payload: GiftPayload):
        super().__init__(payload)
        self.id = payload["id"]
        self.sticker = Sticker(payload["sticker"])
        self.star_count = payload["star_count"]
        self.upgrade_star_count = payload.get("upgrade_star_count", -1)
        self.total_count = payload.get("total_count", 0)
        self.remaining_count = payload.get("remaining_count", 0)


class UniqueGiftModelBase:

    __slots__ = (
        "name",
        "sticker",
        "rarity_per_mille"
    )

    def __init__(self, payload: UniqueGiftModelBasePayload):
        self.name = payload["name"]
        self.sticker = Sticker(payload["sticker"])
        self.rarity_per_mille = payload["rarity_per_mille"]


class UniqueGiftModel(UniqueGiftModelBase):

    def __init__(self, payload: UniqueGiftModelPayload):
        super().__init__(payload)


class UniqueGiftSymbol(UniqueGiftModelBase):

    def __init__(self, payload: UniqueGiftSymbolPayload):
        super().__init__(payload)


class UniqueGiftBackdropColors:

    __slots__ = (
        "center_color",
        "edge_color",
        "symbol_color",
        "text_color"
    )

    def __init__(self, payload: UniqueGiftBackdropColorsPayload):
        self.center_color = payload["center_color"]
        self.edge_color = payload["edge_color"]
        self.symbol_color = payload["symbol_color"]
        self.text_color = payload["text_color"]


class UniqueGiftBackdrop:

    __slots__ = (
        "name",
        "colors",
        "rarity_per_mille"
    )

    def __init__(self, payload: UniqueGiftBackdropPayload):
        self.name = payload["name"]
        self.colors = UniqueGiftBackdropColors(payload["colors"])
        self.rarity_per_mille = payload["rarity_per_mille"]


class UniqueGift(GiftBase):

    __slots__ = (
        "base_name",
        "name",
        "number",
        "model",
        "symbol",
        "backdrop"
    )

    def __init__(self, payload: UniqueGiftPayload):
        super().__init__(payload)
        self.base_name = payload["base_name"]
        self.name = payload["name"]
        self.number = payload["number"]
        self.model = UniqueGiftModel(payload["model"])
        self.symbol = UniqueGiftSymbol(payload["symbol"])
        self.backdrop = UniqueGiftBackdrop(payload["backdrop"])


class GiftInfoBase:

    __slots__ = (
        "owned_gift_id"
    )

    def __init__(self, payload: GiftInfoBasePayload):
        self.owned_gift_id = payload.get("owned_gift_id")


class GiftInfo(GiftInfoBase):

    __slots__ = (
        "gift",
        "convert_star_count",
        "prepaid_upgrade_star_count",
        "can_be_upgraded",
        "text",
        "entities",
        "is_private"
    )

    def __init__(self, payload: GiftInfoPayload):
        super().__init__(payload)
        self.gift = Gift(payload["gift"])
        self.convert_star_count = payload.get("convert_star_count", 0)
        self.prepaid_upgrade_star_count = payload.get("prepaid_upgrade_star_count", 0)
        self.can_be_upgraded = payload.get("can_be_upgraded", False)
        self.text = payload.get("text")
        self.entities = [MessageEntity(e) for e in payload.get("entities", [])]
        self.is_private = payload.get("is_private", False)

    @property
    def can_be_converted(self):
        """
        True if the gift ca be converted to stars.
        """
        return self.convert_star_count != 0


class UniqueGiftInfo(GiftInfoBase):

    __slots__ = (
        "gift",
        "origin",
        "last_resale_star_count",
        "transfer_star_count",
        "next_transfer_date"
    )

    def __init__(self, payload: UniqueGiftInfoPayload):
        super().__init__(payload)
        self.gift = UniqueGift(payload["gift"])
        self.origin = payload["origin"]
        self.last_resale_star_count = payload.get("last_resale_star_count", -1)
        self.transfer_star_count = payload.get("transfer_star_count", -1)
        self.next_transfer_date = payload.get("next_transfer_date", -1)

    @property
    def is_upgraded_gift(self) -> bool:
        """
        True if the unique gift if upgraded from a regular gift.
        """
        return self.origin == "upgrade"

    @property
    def is_transferred_gift(self) -> bool:
        """
        True if the unique gift is transferred from other user or channel.
        """
        return self.origin == "transfer"

    @property
    def is_bought_gift(self) -> bool:
        """
        True if the unique gift was bought from other user.
        """
        return self.origin == "bought"

    @property
    def can_be_transferred(self) -> bool:
        """
        True if the unique gift can be transferred immediately, False otherwise.
        """
        return self.next_transfer_date < datetime.now(tz=UTC).timestamp()
