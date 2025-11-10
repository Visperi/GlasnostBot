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


from typing import List

from typing_extensions import TypedDict, NotRequired

from .media import Sticker
from .chat import Chat
from .message_entity import MessageEntity


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


# TODO: Move
class GiftInfoBase(TypedDict):
    owned_gift_id: NotRequired[str]


# TODO: Move
class GiftInfo(GiftInfoBase):
    gift: Gift
    convert_star_count: NotRequired[int]
    prepaid_upgrade_star_count: NotRequired[int]
    can_be_upgraded: NotRequired[bool]
    text: NotRequired[str]
    entities: NotRequired[List[MessageEntity]]
    is_private: NotRequired[bool]


# TODO: Move
class UniqueGiftInfo(GiftInfoBase):
    gift: UniqueGift
    origin: str
    last_resale_star_count: NotRequired[int]
    transfer_star_count: NotRequired[int]
    next_transfer_date: NotRequired[int]
