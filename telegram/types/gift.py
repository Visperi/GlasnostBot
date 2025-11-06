from typing_extensions import TypedDict, NotRequired

from .media import Sticker
from .chat import Chat


class GiftBase(TypedDict):
    publisher_chat: NotRequired[Chat]


class Gift(GiftBase):
    id: str
    sticker: Sticker
    star_count: int
    upgrade_star_count: NotRequired[int]
    total_count: NotRequired[int]
    remaining_count: NotRequired[int]


class UniqueGiftModelBase(TypedDict):
    name: str
    sticker: Sticker
    rarity_per_mille: int


class UniqueGiftModel(UniqueGiftModelBase):
    pass


class UniqueGiftSymbol(UniqueGiftModelBase):
    pass


class UniqueGiftBackdropColors(TypedDict):
    center_color: int
    edge_color: int
    symbol_color: int
    text_color: int


class UniqueGiftBackdrop(TypedDict):
    name: str
    colors: UniqueGiftBackdropColors
    rarity_per_mille: int


class UniqueGift(GiftBase):
    base_name: str
    name: str
    number: int
    model: UniqueGiftModel
    symbol: UniqueGiftSymbol
    backdrop: UniqueGiftBackdrop
