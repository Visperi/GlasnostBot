from .types.update import Update as UpdatePayload
from .message import Message


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
        self.message = Message(payload.get("message"))
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
