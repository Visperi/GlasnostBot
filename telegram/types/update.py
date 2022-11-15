from typing_extensions import TypedDict, NotRequired
from .message import Message
from .poll import Poll, PollAnswer
from .chat import ChatJoinRequest, ChatMemberUpdated
from .inline_query import (
    InlineQuery,
    ChosenInlineResult,
    CallbackQuery,
    ShippingQuery,
    PreCheckoutQuery
)


class Update(TypedDict):
    update_id: int
    message: NotRequired[Message]
    edited_message: NotRequired[Message]
    channel_post: NotRequired[Message]
    edited_channel_post: NotRequired[Message]
    inline_query: NotRequired[InlineQuery]
    chosen_inline_result: NotRequired[ChosenInlineResult]
    callback_query: NotRequired[CallbackQuery]
    shipping_query: NotRequired[ShippingQuery]
    pre_checkout_query: NotRequired[PreCheckoutQuery]
    poll: NotRequired[Poll]
    poll_answer: NotRequired[PollAnswer]
    my_chat_member: NotRequired[ChatMemberUpdated]
    chat_member: NotRequired[ChatMemberUpdated]
    chat_join_request: NotRequired[ChatJoinRequest]
