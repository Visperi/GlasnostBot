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


from .types.update import Update as UpdatePayload
from .message import Message
from .poll import Poll, PollAnswer
from .chat import ChatMemberUpdated, ChatJoinRequest
from .inline import (
    InlineQuery,
    ChosenInlineResult,
    CallbackQuery,
    PreCheckoutQuery,
    ShippingQuery
)
from .utils import flatten_handlers


@flatten_handlers
class Update:
    _HANDLERS = []

    __slots__ = (
        "update_id",
        "message",
        "edited_message",
        "channel_post",
        "edited_channel_post",
        "inline_query",
        "chosen_inline_result",
        "callback_query",
        "shipping_query",
        "pre_checkout_query",
        "poll",
        "poll_answer",
        "my_chat_member",
        "chat_member",
        "chat_join_request"
    )

    def __init__(self, payload: UpdatePayload) -> None:
        self._update(payload)

    def _update(self, payload: UpdatePayload) -> None:
        self.update_id = payload["update_id"]  # ID is the only required value
        self.message = payload.get("message")
        self.edited_message = payload.get("edited_message")
        self.channel_post = payload.get("channel_post")
        self.edited_channel_post = payload.get("edited_channel_post")
        self.inline_query = payload.get("inline_query")
        self.chosen_inline_result = payload.get("chosen_inline_result")
        self.callback_query = payload.get("callback_query")
        self.shipping_query = payload.get("shipping_query")
        self.pre_checkout_query = payload.get("pre_checkout_query")
        self.poll = payload.get("poll")
        self.poll_answer = payload.get("poll_answer")
        self.my_chat_member = payload.get("my_chat_member")
        self.chat_member = payload.get("chat_member")
        self.chat_join_request = payload.get("chat_join_request")

        for key, func in self._HANDLERS:
            try:
                value = payload[key]  # type: ignore
            except KeyError:
                continue
            else:
                func(self, value)

    def _handle_message(self, value):
        self.message = Message(value)

    def _handle_edited_message(self, value):
        self.edited_message = Message(value)

    def _handle_channel_post(self, value):
        self.channel_post = Message(value)

    def _handle_edited_channel_post(self, value):
        self.edited_channel_post = Message(value)

    def _handle_inline_query(self, value):
        self.inline_query = InlineQuery(value)

    def _handle_chosen_inline_result(self, value):
        self.chosen_inline_result = ChosenInlineResult(value)

    def _handle_callback_query(self, value):
        self.callback_query = CallbackQuery(value)

    def _handle_shipping_query(self, value):
        self.shipping_query = ShippingQuery(value)

    def _handle_pre_checkout_query(self, value):
        self.pre_checkout_query = PreCheckoutQuery(value)

    def _handle_poll(self, value):
        self.poll = Poll(value)

    def _handle_poll_answer(self, value):
        self.poll_answer = PollAnswer(value)

    def _handle_my_chat_member(self, value):
        self.my_chat_member = ChatMemberUpdated(value)

    def _handle_chat_member(self, value):
        self.chat_member = ChatMemberUpdated(value)

    def _handle_chat_join_request(self, value):
        self.chat_join_request = ChatJoinRequest(value)
