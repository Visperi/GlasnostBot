"""
MIT License

Copyright (c) 2025 Niko Mätäsaho

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


from .types.business import (
    BusinessBotRights as BusinessBotRightsPayload,
    BusinessConnection as BusinessConnectionPayload,
    BusinessMessagesDeleted as BusinessMessagesDeletedPayload,
)
from .chat import Chat


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