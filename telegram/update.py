from .types.update import Update as UpdatePayload
from .message import Message
from .poll import Poll, PollAnswer
from .chat import ChatMemberUpdated, ChatJoinRequest
from .inline_query import (
    InlineQuery,
    ChosenInlineResult,
    CallbackQuery,
    PreCheckoutQuery,
    ShippingQuery
)


class Update:

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
        self.__update(payload)

    def __update(self, payload: UpdatePayload) -> None:
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

        for slot in (
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
        ):
            try:
                getattr(self, f"__handle_{slot}")(payload[slot])  # type: ignore
            except KeyError:
                pass

    def __handle_message(self, value):
        self.message = Message(value)

    def __handle_edited_message(self, value):
        self.edited_message = Message(value)

    def __handle_channel_post(self, value):
        self.channel_post = Message(value)

    def __handle_edited_channel_post(self, value):
        self.edited_channel_post = Message(value)

    def __handle_inline_query(self, value):
        self.inline_query = InlineQuery(value)

    def __handle_chosen_inline_result(self, value):
        self.chosen_inline_result = ChosenInlineResult(value)

    def __handle_callback_query(self, value):
        self.callback_query = CallbackQuery(value)

    def __handle_shipping_query(self, value):
        self.shipping_query = ShippingQuery(value)

    def __handle_pre_checkout_query(self, value):
        self.pre_checkout_query = PreCheckoutQuery(value)

    def __handle_poll(self, value):
        self.poll = Poll(value)

    def __handle_poll_answer(self, value):
        self.poll_answer = PollAnswer(value)

    def __handle_my_chat_member(self, value):
        self.my_chat_member = ChatMemberUpdated(value)

    def __handle_chat_member(self, value):
        self.chat_member = ChatMemberUpdated(value)

    def __handle_chat_join_request(self, value):
        self.chat_join_request = ChatJoinRequest(value)
