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


from .types.user import (
    User as UserPayload,
    SharedUser as SharedUserPayload,
    UsersShared as UsersSharedPayload,
    WriteAccessAllowed as WriteAccessAllowedPayload,
    BusinessBotRights as BusinessBotRightsPayload,
    BusinessConnection as BusinessConnectionPayload,
    BusinessMessagesDeleted as BusinessMessagesDeletedPayload,
    ChatShared as ChatSharedPayload
)
from .media import PhotoSize
from .chat import Chat


class User:

    __slots__ = (
        "id",
        "is_bot",
        "first_name",
        "last_name",
        "username",
        "language_code",
        "is_premium",
        "added_to_attachment_menu",
        "can_join_groups",
        "can_read_all_group_messages",
        "supports_inline_queries"
    )

    def __init__(self, payload: UserPayload) -> None:
        self.id = payload["id"]
        self.is_bot = payload["is_bot"]
        self.first_name = payload["first_name"]
        self.last_name = payload.get("last_name")
        self.username = payload.get("username")
        self.language_code = payload.get("language_code")
        self.is_premium = payload.get("is_premium", False)
        self.added_to_attachment_menu = payload.get("added_to_attachment_menu", False)
        self.can_join_groups = payload.get("can_join_groups", False)
        self.can_read_all_group_messages = payload.get("can_read_all_group_messages", False)
        self.supports_inline_queries = payload.get("supports_inline_queries", False)


class SharedUser:

    __slots__ = (
        "user_id",
        "first_name",
        "last_name",
        "username",
        "photo"
    )

    def __init__(self, payload: SharedUserPayload):
        self.user_id = payload["user_id"]
        self.first_name = payload.get("first_name")
        self.last_name = payload.get("last_name")
        self.username = payload.get("username")
        self.photo = payload.get("photo", [])

        self.photo = [PhotoSize(p) for p in payload["photo"]]


class UsersShared:

    __slots__ = (
        "request_id",
        "users"
    )

    def __init__(self, payload: UsersSharedPayload):
        self.request_id = payload["request_id"]
        self.users = payload.get("users", [])

        self.users = [SharedUser(s) for s in self.users]


class WriteAccessAllowed:

    __slots__ = (
        "from_request",
        "web_app_name",
        "from_attachment_menu"
    )

    def __init__(self, payload: WriteAccessAllowedPayload):
        self.from_request = payload.get("from_request")
        self.web_app_name = payload.get("web_app_name")
        self.from_attachment_menu = payload.get("from_attachment_menu")


class BusinessBotRights:

    __slots__ = (
        "can_reply",
        "can_read_messages",
        "can_delete_sent_messages",
        "can_delete_all_messages",
        "can_edit_name",
        "can_edit_bio",
        "can_edit_profile_photo",
        "can_edit_username",
        "can_change_gift_settings",
        "can_view_gifts_and_stars",
        "can_convert_gifts_to_stars",
        "can_transfer_and_upgrade_gifts",
        "can_transfer_stars",
        "can_manage_stories"
    )

    def __init__(self, payload: BusinessBotRightsPayload):
        for attr in self.__slots__:
            setattr(self, attr, payload.get(attr, False))  # type: ignore


class BusinessConnection:

    __slots__ = (
        "id",
        "user",
        "user_chat_id",
        "date",
        "rights",
        "is_enabled"
    )

    def __init__(self, payload: BusinessConnectionPayload):
        self.id = payload["id"]
        self.user = payload["user"]
        self.user_chat_id = payload["user_chat_id"]
        self.date = payload["date"]
        self.is_enabled = payload["is_enabled"]

        try:
            self.rights = BusinessBotRights(payload["rights"])
        except KeyError:
            self.rights = None


class BusinessMessagesDeleted:

    __slots__ = (
        "business_connection_id",
        "chat",
        "message_ids"
    )

    def __init__(self, payload: BusinessMessagesDeletedPayload):
        self.business_connection_id = payload["business_connection_id"]
        self.chat = Chat(payload["chat"])
        self.message_ids = payload["message_ids"]


class ChatShared:

    __slots__ = (
        "request_id",
        "chat_id",
        "title",
        "username",
        "photo"
    )

    def __init__(self, payload: ChatSharedPayload):
        self.request_id = payload["request_id"]
        self.chat_id = payload["chat_id"]
        self.title = payload.get("title")
        self.username = payload.get("username")
        self.photo = payload.get("photo", [])

        self.photo = [PhotoSize(p) for p in self.photo]
