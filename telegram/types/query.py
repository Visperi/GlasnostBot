from typing_extensions import TypedDict, NotRequired

from .user import User
from .location import Location
from .message import MaybeInaccessibleMessage
from .payments import OrderInfo, ShippingAddress


class InlineQueryBase(TypedDict):
    id: str
    from_: User


class InlineQuery(InlineQueryBase):
    query: str
    offset: str
    chat_type: NotRequired[str]
    location: NotRequired[Location]


class CallbackQuery(InlineQueryBase):
    message: NotRequired[MaybeInaccessibleMessage]
    inline_message_id: NotRequired[str]
    chat_instance: str
    data: NotRequired[str]
    game_short_name: NotRequired[str]


class AnswerCallbackQuery(TypedDict):
    callback_query_id: str
    text: NotRequired[str]
    show_alert: NotRequired[bool]
    url: NotRequired[str]
    cache_time: NotRequired[int]


class ShippingQuery(InlineQueryBase):
    invoice_payload: str
    shipping_address: ShippingAddress


class PreCheckoutQuery(InlineQueryBase):
    currency: str
    total_amount: int
    invoice_payload: str
    shipping_option_id: NotRequired[str]
    order_info: NotRequired[OrderInfo]


class ChosenInlineResult(TypedDict):
    result_id: str
    from_: User
    location: NotRequired[Location]
    inline_message_id: NotRequired[str]
    query: NotRequired[str]
