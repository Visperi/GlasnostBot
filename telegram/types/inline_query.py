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

from typing import List

from typing_extensions import TypedDict, NotRequired

from .user import User
from .location import Location
from .message import MaybeInaccessibleMessage
from .web_app import WebAppInfo


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


class ChosenInlineResult(TypedDict):
    result_id: str
    from_: User
    location: NotRequired[Location]
    inline_message_id: NotRequired[str]
    query: NotRequired[str]


class LoginUrl(TypedDict):
    url: str
    forward_text: NotRequired[str]
    bot_username: NotRequired[str]
    request_write_access: NotRequired[bool]


class SwitchInlineQueryChosenChat(TypedDict):
    query: NotRequired[str]
    allow_user_chats: NotRequired[bool]
    allow_bot_chats: NotRequired[bool]
    allow_group_chats: NotRequired[bool]
    allow_channel_posts: NotRequired[bool]


class CopyTextButton(TypedDict):
    text: str


class CallbackGame(TypedDict):
    pass


class InlineKeyboardButton(TypedDict):
    text: str
    url: NotRequired[str]
    callback_data: NotRequired[str]
    web_app: NotRequired[WebAppInfo]
    login_url: NotRequired[LoginUrl]
    switch_inline_query: NotRequired[str]
    switch_inline_query_current_chat: NotRequired[SwitchInlineQueryChosenChat]
    copy_text: NotRequired[CopyTextButton]
    callback_game: NotRequired[CallbackGame]
    pay: NotRequired[bool]


class InlineKeyboardMarkup(TypedDict):
    inline_keyboard: List[InlineKeyboardButton]
