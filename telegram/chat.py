from .types.chat import Chat as ChatPayload


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
