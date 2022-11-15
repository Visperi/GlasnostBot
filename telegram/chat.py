from .message import Message
from .location import Location
from .types.chat import (
    Chat as ChatPayload,
    ChatPhoto as ChatPhotoPayload,
    ChatLocation as ChatLocationPayload,
    ChatPermissions as ChatPermissionsPayload)


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
        self.__update(payload)

    def __update(self, payload: ChatPayload) -> None:
        self.id = payload["id"]
        self.type = payload["type"]
        self.title = payload.get("title")
        self.username = payload.get("username")
        self.first_name = payload.get("first_name")
        self.last_name = payload.get("last_name")
        self.bio = payload.get("bio")
        self.has_private_forwards = payload.get("has_private_forwards", False)
        self.has_restricted_voice_and_video_messages = payload.get("has_restricted_voice_and_video_messages", False)
        self.join_to_send_messages = payload.get("join_to_send_messages", False)
        self.join_by_request = payload.get("join_by_request", False)
        self.description = payload.get("description")
        self.invite_link = payload.get("invite_link")
        self.slow_mode_delay = payload.get("slow_mode_delay", -1)
        self.message_auto_delete_time = payload.get("message_auto_delete_time", -1)
        self.has_protected_content = payload.get("has_protected_content", False)
        self.sticker_set_name = payload.get("sticker_set_name")
        self.can_set_sticker_set = payload.get("can_set_sticker_set", False)
        self.linked_chat_id = payload.get("linked_chat_id", -1)

        for slot in ("photo", "pinned_message", "permissions", "location"):
            try:
                value = payload[slot]
                getattr(self, f"__handle_{slot}")(value)
            except KeyError:
                continue

    def __handle_photo(self, value):
        self.photo = ChatPhoto(value)

    def __handle_pinned_message(self, value):
        self.pinned_message = Message(value)

    def __handle_permissions(self, value):
        self.permissions = ChatPermissions(value)

    def __handle_location(self, value):
        self.location = ChatLocation(value)
