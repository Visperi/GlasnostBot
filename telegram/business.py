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