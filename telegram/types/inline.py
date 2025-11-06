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


class WriteAccessAllowed(TypedDict):
    from_request: NotRequired[bool]
    web_app_name: NotRequired[str]
    from_attachment_menu: NotRequired[bool]


class WebAppData(TypedDict):
    data: str
    button_text: str


class WebAppInfo(TypedDict):
    url: str


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
