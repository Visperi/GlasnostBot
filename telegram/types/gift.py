from typing import List

from typing_extensions import TypedDict, NotRequired

from .message import MessageEntity
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


class GiftInfoBase(TypedDict):
    owned_gift_id: NotRequired[str]


class GiftInfo(GiftInfoBase):
    gift: Gift
    convert_star_count: NotRequired[int]
    prepaid_upgrade_star_count: NotRequired[int]
    can_be_upgraded: NotRequired[bool]
    text: NotRequired[str]
    entities: NotRequired[List[MessageEntity]]
    is_private: NotRequired[bool]


class UniqueGiftInfo(GiftInfoBase):
    gift: UniqueGift
    origin: str
    last_resale_star_count: NotRequired[int]
    transfer_star_count: NotRequired[int]
    next_transfer_date: NotRequired[int]
