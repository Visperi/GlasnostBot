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
