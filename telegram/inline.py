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

from .utils import flatten_handlers
from .types.inline import (
    InlineQueryBase as InlineQueryBasePayload,
    InlineQuery as InlineQueryPayload,
    CallbackQuery as CallbackQueryPayload,
    ShippingQuery as ShippingQueryPayload,
    PreCheckoutQuery as PreCheckoutQueryPayload,
    ChosenInlineResult as ChosenInlineResultPayload,
    AnswerCallbackQuery as AnswerCallbackQueryPayload,
    LoginUrl as LoginUrlPayload,
    WebAppData as WebAppDataPayload,
    WebAppInfo as WebAppInfoPayload,
    InlineKeyboardButton as InlineKeyboardButtonPayload,
    CopyTextButton as CopyTextButtonPayload,
    SwitchInlineQueryChosenChat as SwitchInlineQueryChosenChatPayload
)
from .user import User
from .location import Location
from .message import MaybeInaccessibleMessage
from .payments import OrderInfo, ShippingAddress


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
        self.inline_message_id = payload.get("inline_message_id")
        self.chat_instance = payload["chat_instance"]
        self.data = payload.get("data")
        self.game_short_name = payload.get("game_short_name")

        try:
            self.message = (MaybeInaccessibleMessage(payload["message"]))
        except KeyError:
            self.message = None


class AnswerCallbackQuery:

    __slots__ = (
        "callback_query_id",
        "text",
        "show_alert",
        "url",
        "cache_time"
    )

    def __init__(self, payload: AnswerCallbackQueryPayload):
        self.callback_query_id = payload["callback_query_id"]
        self.text = payload.get("text")
        self.show_alert = payload.get("show_alert")
        self.url = payload.get("url")
        self.cache_time = payload.get("cache_time", -1)


class ShippingQuery(InlineQueryBase):

    __slots__ = (
        "invoice_payload",
        "shipping_address"
    )

    def __init__(self, payload: ShippingQueryPayload):
        super().__init__(payload)
        self.invoice_payload = payload["invoice_payload"]
        self.shipping_address = ShippingAddress(payload["shipping_address"])


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
        self.result_id = payload["result_id"]
        self.from_ = User(payload["from_"])
        self.inline_message_id = payload.get("inline_message_id")
        self.query = payload.get("query")

        try:
            self.location = Location(payload["location"])
        except KeyError:
            self.location = None


class LoginUrl:

    __slots__ = (
        "url",
        "forward_text",
        "bot_username",
        "request_write_access"
    )

    def __init__(self, payload: LoginUrlPayload):
        self.url = payload["url"]
        self.forward_text = payload.get("forward_text")
        self.bot_username = payload.get("bot_username")
        self.request_write_access = payload.get("request_write_access", False)


class SwitchInlineQueryChosenChat:

    __slots__ = (
        "query",
        "allow_user_chats",
        "allow_bot_chats",
        "allow_group_chats",
        "allow_channel_posts"
    )

    def __init__(self, payload: SwitchInlineQueryChosenChatPayload):
        self.query = payload.get("query")
        self.allow_user_chats = payload.get("allow_user_chats", False)
        self.allow_bot_chats = payload.get("allow_bot_chats", False)
        self.allow_group_chats = payload.get("allow_group_chats", False)
        self.allow_channel_posts = payload.get("allow_channel_posts", False)


class CopyTextButton:

    __slots__ = (
        "text"
    )

    def __init__(self, payload: CopyTextButtonPayload):
        self.text = payload["text"]


class CallbackGame:
    """
    Reserver by Telegram API.
    """
    def __init__(self, payload):
        pass


class WebAppData:

    __slots__ = (
        "data",
        "button_text"
    )

    def __init__(self, payload: WebAppDataPayload):
        self.data = payload["data"]
        self.button_text = payload["button_text"]


class WebAppInfo:

    __slots__ = (
        "url"
    )

    def __init__(self, payload: WebAppInfoPayload):
        self.url = payload["url"]


@flatten_handlers
class InlineKeyboardButton:
    _HANDLERS = []

    __slots__ = (
        "text",
        "url",
        "callback_data",
        "web_app",
        "login_url",
        "switch_inline_query",
        "switch_inline_query_current_chat",
        "copy_text",
        "callback_game",
        "pay"
    )

    def __init__(self, payload: InlineKeyboardButtonPayload):
        self.text = payload["text"]
        self.url = payload.get("url")
        self.callback_data = payload.get("callback_data")
        self.web_app = payload.get("web_app")
        self.login_url = payload.get("login_url")
        self.switch_inline_query = payload.get("switch_inline_query")
        self.switch_inline_query_current_chat = payload.get("switch_inline_query_current_chat")
        self.copy_text = payload.get("copy_text")
        self.callback_game = payload.get("callback_game")
        self.pay = payload.get("pay", False)

        for key, func in self._HANDLERS:
            try:
                value = payload[key]  # type: ignore
            except KeyError:
                continue
            else:
                func(self, value)

    def _handle_web_app(self, value):
        self.web_app = WebAppInfo(value)

    def _handle_switch_inline_query_current_chat(self, value):
        self.switch_inline_query_current_chat = SwitchInlineQueryChosenChat(value)

    def _handle_copy_text(self, value):
        self.copy_text = CopyTextButton(value)

    def _handle_callback_game(self, value):
        self.callback_game = CallbackGame(value)
