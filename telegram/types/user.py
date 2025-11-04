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

from .media import PhotoSize
from .chat import Chat


class User(TypedDict):
    id: int
    is_bot: bool
    first_name: str
    last_name: NotRequired[str]
    username: NotRequired[str]
    language_code: NotRequired[str]
    is_premium: NotRequired[bool]
    added_to_attachment_menu: NotRequired[bool]
    can_join_groups: NotRequired[bool]
    can_read_all_group_messages: NotRequired[bool]
    supports_inline_queries: NotRequired[bool]


class SharedUser(TypedDict):
    user_id: int
    first_name: NotRequired[str]
    last_name: NotRequired[str]
    username: NotRequired[str]
    photo: NotRequired[List[PhotoSize]]


class UsersShared(TypedDict):
    request_id: int
    users: List[SharedUser]


class WriteAccessAllowed(TypedDict):
    from_request: NotRequired[bool]
    web_app_name: NotRequired[str]
    from_attachment_menu: NotRequired[bool]


class BusinessBotRights(TypedDict):
    can_reply: NotRequired[bool]
    can_read_messages: NotRequired[bool]
    can_delete_sent_messages: NotRequired[bool]
    can_delete_all_messages: NotRequired[bool]
    can_edit_name: NotRequired[bool]
    can_edit_bio: NotRequired[bool]
    can_edit_profile_photo: NotRequired[bool]
    can_edit_username: NotRequired[bool]
    can_change_gift_settings: NotRequired[bool]
    can_view_gifts_and_stars: NotRequired[bool]
    can_convert_gifts_to_stars: NotRequired[bool]
    can_transfer_and_upgrade_gifts: NotRequired[bool]
    can_transfer_stars: NotRequired[bool]
    can_manage_stories: NotRequired[bool]


class BusinessConnection(TypedDict):
    id: str
    user: User
    user_chat_id: int
    date: int
    rights: NotRequired[BusinessBotRights]
    is_enabled: bool


class BusinessMessagesDeleted(TypedDict):
    business_connection_id: str
    chat: Chat
    message_ids: List[int]


class ChatShared(TypedDict):
    request_id: int
    chat_id: int
    title: NotRequired[str]
    username: NotRequired[str]
    photo: NotRequired[List[PhotoSize]]
