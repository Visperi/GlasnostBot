from typing_extensions import TypedDict, NotRequired
from .user import User
from .location import Location
from .message import Message
from .payments import ShippingAddress, OrderInfo


class InlineQueryBase(TypedDict):
    id: str
    from_: User


class InlineQuery(InlineQueryBase):
    query: str
    offset: str
    chat_type: NotRequired[str]
    location: NotRequired[Location]


class CallbackQuery(InlineQueryBase):
    message: NotRequired[Message]
    inline_message_id: NotRequired[str]
    chat_instance: str
    data: NotRequired[str]
    game_short_name: NotRequired[str]


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
