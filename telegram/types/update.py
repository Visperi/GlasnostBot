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


from typing_extensions import TypedDict, NotRequired
from .message import Message, MessageReactionUpdated, MessageReactionCountUpdated
from .poll import Poll, PollAnswer
from .chat import ChatJoinRequest, ChatMemberUpdated
from .chat_boost import ChatBoostUpdated, ChatBoostRemoved
from .user import BusinessConnection, BusinessMessagesDeleted
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
    business_connection: NotRequired[BusinessConnection]
    business_message: NotRequired[Message]
    edited_business_message: NotRequired[Message]
    deleted_business_messages: NotRequired[BusinessMessagesDeleted]
    message_reaction: NotRequired[MessageReactionUpdated]
    message_reaction_count: NotRequired[MessageReactionCountUpdated]
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
    chat_boost: NotRequired[ChatBoostUpdated]
    removed_chat_boost: NotRequired[ChatBoostRemoved]
