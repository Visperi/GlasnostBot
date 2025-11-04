from typing import List

from typing_extensions import TypedDict, NotRequired

from .chat import Chat
from .user import User
from .document import PhotoSize


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
