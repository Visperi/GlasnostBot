from .types.gift import (
    GiftBase as GiftBasePayload,
    Gift as GiftPayload,
    UniqueGiftModelBase as UniqueGiftModelBasePayload,
    UniqueGiftModel as UniqueGiftModelPayload,
    UniqueGiftSymbol as UniqueGiftSymbolPayload,
    UniqueGiftBackdropColors as UniqueGiftBackdropColorsPayload,
    UniqueGiftBackdrop as UniqueGiftBackdropPayload,
    UniqueGift as UniqueGiftPayload
)
from .chat import Chat
from .media import Sticker


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
        self.total_count = payload.get("total_count", -1)
        self.remaining_count = payload.get("remaining_count", -1)


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
