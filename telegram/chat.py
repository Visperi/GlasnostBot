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


from typing_extensions import TYPE_CHECKING
from .location import Location
from .user import User
from .types.chat import (
    Chat as ChatPayload,
    ChatPhoto as ChatPhotoPayload,
    ChatMember as ChatMemberPayload,
    ChatLocation as ChatLocationPayload,
    ChatInviteLink as ChatInviteLinkPayload,
    ChatPermissions as ChatPermissionsPayload,
    ChatJoinRequest as ChatJoinRequestPayload,
    ChatMemberUpdated as ChatMemberUpdatedPayload
)
from .utils import flatten_handlers


if TYPE_CHECKING:
    from .message import Message


class ChatPhoto:

    __slots__ = (
        "small_file_id",
        "small_file_unique_id",
        "big_file_id",
        "big_file_unique_id"
    )

    def __init__(self, payload: ChatPhotoPayload):
        self.small_file_id = payload["small_file_id"]
        self.small_file_unique_id = payload["small_file_unique_id"]
        self.big_file_id = payload["big_file_id"]
        self.big_file_unique_id = payload["big_file_unique_id"]


class ChatLocation:

    def __init__(self, payload: ChatLocationPayload):
        self.location = Location(payload["location"])
        self.address = payload["address"]


class ChatPermissions:

    __slots__ = (
        "can_send_messages",
        "can_send_media_messages",
        "can_send_polls",
        "can_send_other_messages",
        "can_add_web_page_previews",
        "can_change_info",
        "can_invite_users",
        "can_pin_messages"
    )

    def __init__(self, payload: ChatPermissionsPayload):
        self.can_send_messages = payload.get("can_send_messages", False)
        self.can_send_media_messages = payload.get("can_send_media_messages", False)
        self.can_send_polls = payload.get("can_send_polls", False)
        self.can_send_other_messages = payload.get("can_send_other_messages", False)
        self.can_add_web_page_previews = payload.get("can_add_web_page_previews", False)
        self.can_change_info = payload.get("can_change_info", False)
        self.can_invite_users = payload.get("can_invite_users", False)
        self.can_pin_messages = payload.get("can_pin_messages", False)


@flatten_handlers
class Chat:

    __slots__ = (
        "id",
        "type",
        "title",
        "username",
        "first_name",
        "last_name",
        "photo",
        "bio",
        "has_private_forwards",
        "has_restricted_voice_and_video_messages",
        "join_to_send_messages",
        "join_by_request",
        "description",
        "invite_link",
        "pinned_message",
        "permissions",
        "slow_mode_delay",
        "message_auto_delete_time",
        "has_protected_content",
        "sticker_set_name",
        "can_set_sticker_set",
        "linked_chat_id",
        "location"
    )

    def __init__(self, payload: ChatPayload) -> None:
        self._update(payload)

    def _update(self, payload: ChatPayload) -> None:
        self.id = payload["id"]
        self.type = payload["type"]
        self.title = payload.get("title")
        self.username = payload.get("username")
        self.first_name = payload.get("first_name")
        self.last_name = payload.get("last_name")
        self.photo = payload.get("photo")
        self.bio = payload.get("bio")
        self.has_private_forwards = payload.get("has_private_forwards", False)
        self.has_restricted_voice_and_video_messages = payload.get("has_restricted_voice_and_video_messages", False)
        self.join_to_send_messages = payload.get("join_to_send_messages", False)
        self.join_by_request = payload.get("join_by_request", False)
        self.description = payload.get("description")
        self.invite_link = payload.get("invite_link")
        self.pinned_message = payload.get("pinned_message")
        self.permissions = payload.get("permissions")
        self.slow_mode_delay = payload.get("slow_mode_delay", -1)
        self.message_auto_delete_time = payload.get("message_auto_delete_time", -1)
        self.has_protected_content = payload.get("has_protected_content", False)
        self.sticker_set_name = payload.get("sticker_set_name")
        self.can_set_sticker_set = payload.get("can_set_sticker_set", False)
        self.linked_chat_id = payload.get("linked_chat_id", -1)
        self.location = payload.get("location")

        for key, func in self._HANDLERS:
            try:
                value = payload[key]  # type: ignore
            except KeyError:
                continue
            else:
                func(self, value)

    def _handle_photo(self, value):
        self.photo = ChatPhoto(value)

    def _handle_pinned_message(self, value):
        self.pinned_message = Message(value)

    def _handle_permissions(self, value):
        self.permissions = ChatPermissions(value)

    def _handle_location(self, value):
        self.location = ChatLocation(value)


class ChatInviteLink:

    __slots__ = (
        "invite_link",
        "creator",
        "creates_join_request",
        "is_primary",
        "is_revoked",
        "name",
        "expire_date",
        "member_limit",
        "pending_join_request_count"
    )

    def __init__(self, payload: ChatInviteLinkPayload):
        self.invite_link = payload["invite_link"]
        self.creator = User(payload["creator"])
        self.creates_join_request = payload["creates_join_request"]
        self.is_primary = payload["is_primary"]
        self.is_revoked = payload["is_revoked"]
        self.name = payload.get("name")
        self.expire_date = payload.get("expire_date", -1)
        self.member_limit = payload.get("member_limit", -1)
        self.pending_join_request_count = payload.get("pending_join_request_count", -1)


class ChatJoinRequest:

    __slots__ = (
        "chat",
        "from_",
        "date",
        "bio",
        "invite_link"
    )

    # TODO: Figure out how to read variable 'from' to 'from_' from payload!
    def __init__(self, payload: ChatJoinRequestPayload):
        self.chat = Chat(payload["chat"])
        self.from_ = User(payload["from_"])
        self.date = payload["date"]
        self.bio = payload.get("bio")
        self.invite_link = ChatInviteLink(payload["invite_link"])


class ChatMember:

    __slots__ = (
        "status",
        "user"
    )

    def __init__(self, payload: ChatMemberPayload):
        self.status = payload["status"]
        self.user = User(payload["user"])


class ChatMemberUpdated:

    __slots__ = (
        "chat",
        "from_",
        "date",
        "old_chat_member",
        "new_chat_member",
        "invite_link"
    )

    # TODO: Figure out how to read variable 'from' to 'from_' from payload!

    def __init__(self, payload: ChatMemberUpdatedPayload):
        self.chat = Chat(payload["chat"])
        self.from_ = User(payload["from_"])
        self.date = payload["date"]
        self.old_chat_member = ChatMember(payload["old_chat_member"])
        self.new_chat_member = ChatMember(payload["old_chat_member"])

        try:
            self.invite_link = ChatInviteLink(payload["invite_link"])
        except KeyError:
            self.invite_link = None
