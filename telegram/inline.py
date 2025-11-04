"""
MIT License

Copyright (c) 2022 Niko Mätäsaho

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


from .types.inline import (
    InlineQueryBase as InlineQueryBasePayload,
    InlineQuery as InlineQueryPayload,
    CallbackQuery as CallbackQueryPayload,
    ShippingQuery as ShippingQueryPayload,
    PreCheckoutQuery as PreCheckoutQueryPayload,
    ChosenInlineResult as ChosenInlineResultPayload
)
from .user import User
from .location import Location
from .message import Message
from .payments import OrderInfo


class InlineQueryBase:

    __slots__ = (
        "id",
        "from_"
    )

    def __init__(self, payload: InlineQueryBasePayload):
        self.id = payload["id"]
        self.from_ = User(payload["from_"])


class InlineQuery(InlineQueryBase):

    __slots__ = (
        "query",
        "offset",
        "chat_type",
        "location"
    )

    def __init__(self, payload: InlineQueryPayload):
        super().__init__(payload)
        self._update(payload)

    def _update(self, payload: InlineQueryPayload):
        self.query = payload["query"]
        self.offset = payload["offset"]
        self.chat_type = payload.get("chat_type")

        try:
            self.location = Location(payload["location"])
        except KeyError:
            self.location = None


class CallbackQuery(InlineQueryBase):

    __slots__ = (
        "message",
        "inline_message_id",
        "chat_instance",
        "data",
        "game_short_name"
    )

    def __init__(self, payload: CallbackQueryPayload):
        super().__init__(payload)
        self._update(payload)

    def _update(self, payload: CallbackQueryPayload):
        self.inline_message_id = payload.get("inline_message_id")
        self.chat_instance = payload["chat_instance"]
        self.data = payload.get("data")
        self.game_short_name = payload.get("game_short_name")

        try:
            self.message = Message(payload["message"])
        except KeyError:
            self.message = None


class ShippingQuery(InlineQueryBase):

    __slots__ = (
        "invoice_payload",
        "shipping_address"
    )

    def __init__(self, payload: ShippingQueryPayload):
        super().__init__(payload)
        self._update(payload)

    def _update(self, payload: ShippingQueryPayload):
        self.invoice_payload = payload["invoice_payload"]
        self.shipping_address = payload["shipping_address"]


class PreCheckoutQuery(InlineQueryBase):

    __slots__ = (
        "currency",
        "total_amount",
        "invoice_payload",
        "shipping_option_id",
        "order_info"
    )

    def __init__(self, payload: PreCheckoutQueryPayload):
        super().__init__(payload)
        self._update(payload)

    # noinspection Duplicates
    def _update(self, payload: PreCheckoutQueryPayload):
        self.currency = payload["currency"]
        self.total_amount = payload["total_amount"]
        self.invoice_payload = payload["invoice_payload"]
        self.shipping_option_id = payload.get("shipping_option_id")

        try:
            self.order_info = OrderInfo(payload["order_info"])
        except KeyError:
            self.order_info = None


class ChosenInlineResult:

    __slots__ = (
        "result_id",
        "from_",
        "location",
        "inline_message_id",
        "query"
    )

    def __init__(self, payload: ChosenInlineResultPayload):
        self._update(payload)

    def _update(self, payload: ChosenInlineResultPayload):
        self.result_id = payload["result_id"]
        self.from_ = payload["from_"]
        self.inline_message_id = payload.get("inline_message_id")
        self.query = payload.get("query")

        try:
            self.location = Location(payload["location"])
        except KeyError:
            self.location = None
