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


from .user import User
from .types.chat import (
    Chat as ChatPayload,
    ChatPhoto as ChatPhotoPayload,
    ChatMember as ChatMemberPayload,
    ChatInviteLink as ChatInviteLinkPayload,
    ChatPermissions as ChatPermissionsPayload,
    ChatJoinRequest as ChatJoinRequestPayload,
    ChatMemberUpdated as ChatMemberUpdatedPayload,
    ChatBackground as ChatBackgroundPayload,
    VideoChatScheduled as VideoChatScheduledPayload,
    VideoChatEnded as VideoChatEndedPayload,
    VideoChatParticipantsInvited as VideoChatParticipantsInvitedPayload,
    ChatMemberOwner as ChatMemberOwnerPayload,
    ChatMemberAdministrator as ChatMemberAdministratorPayload,
    ChatMemberMember as ChatMemberMemberPayload,
    ChatMemberRestricted as ChatMemberRestrictedPayload,
    ChatMemberLeft as ChatMemberLeftPayload,
    ChatMemerBanned as ChatMemberBannedPayload,
    Story as StoryPayload,
)


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


class ChatPermissions:

    __slots__ = (
        "can_send_messages",
        "can_send_audios",
        "can_send_documents",
        "can_send_photos",
        "can_send_videos",
        "can_send_video_notes",
        "can_send_voice_notes",
        "can_send_polls",
        "can_send_other_messages",
        "can_add_web_page_previews",
        "can_change_info",
        "can_invite_users",
        "can_pin_messages",
        "can_manage_topics"
    )

    def __init__(self, payload: ChatPermissionsPayload):
        for attr_name in self.__slots__:
            setattr(self, attr_name, payload.get(attr_name, False))  # type: ignore

        # According to API documentation, this defaults to can_pin_messages if omitted
        self.can_manage_topics = payload.get("can_manage_topics", self.can_pin_messages)


class Chat:

    __slots__ = (
        "id",
        "type",
        "title",
        "username",
        "first_name",
        "last_name",
        "is_forum",
        "is_direct_messages"
    )

    def __init__(self, payload: ChatPayload) -> None:
        """
        Represents a chat in Telegram.

        :param payload: A dictionary payload from Telegram API.
        """

        self.id = payload["id"]
        """
        Unique identifier for the chat.
        """
        self.type = payload["type"]
        """
        Type of the chat. Can have values private, group, supergroup or channel.
        """
        self.title = payload.get("title")
        """
        Title for groups, superchannels and channels.
        """
        self.username = payload.get("username")
        """
        Username for private chats, supergroups and channels if available.
        """
        self.first_name = payload.get("first_name")
        """
        First name of the other party in private chats.
        """
        self.last_name = payload.get("last_name")
        """
        Last name of the other party in private chats.
        """
        self.is_forum = payload.get("is_forum", False)
        """
        True if the chat is a supergroup and has topics enabled, being a forum.
        """
        self.is_direct_messages = payload.get("is_direct_messages", False)
        """
        True if the chat is a direct messages chat of a channel.
        """


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
        "pending_join_request_count",
        "subscription_period",
        "subscription_price"
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
        self.pending_join_request_count = payload.get("pending_join_request_count", 0)
        self.subscription_period = payload.get("subscription_period", -1)
        self.subscription_price = payload.get("subscription_price", -1)

class ChatJoinRequest:

    __slots__ = (
        "chat",
        "from_",
        "user_chat_id",
        "date",
        "bio",
        "invite_link"
    )

    def __init__(self, payload: ChatJoinRequestPayload):
        self.chat = Chat(payload["chat"])
        self.from_ = User(payload["from_"])
        self.user_chat_id = payload["user_chat_id"]
        self.date = payload["date"]
        self.bio = payload.get("bio")

        try:
            self.invite_link = ChatInviteLink(payload["invite_link"])
        except KeyError:
            self.invite_link = None


# TODO: Refactor ChatMember classes
class ChatMember:

    __slots__ = (
        "status",
        "user"
    )

    def __init__(self, payload: ChatMemberPayload):
        self.status = payload["status"]
        self.user = User(payload["user"])


class ChatMemberOwner(ChatMember):

    __slots__ = (
        "is_anonymous",
        "custom_title"
    )

    def __init__(self, payload: ChatMemberOwnerPayload):
        super().__init__(payload)
        self.is_anonymous = payload["is_anonymous"]
        self.custom_title = payload.get("custom_title")


class ChatMemberAdministrator(ChatMember):

    __slots__ = (
        "can_be_edited",
        "is_anonymous",
        "can_manage_chat",
        "can_delete_messages",
        "can_manage_video_chats",
        "can_restrict_members",
        "can_promote_members",
        "can_change_info",
        "can_invite_users",
        "can_post_stories",
        "can_edit_stories",
        "can_delete_stories",
        "can_post_messages",
        "can_edit_messages",
        "can_pin_messages",
        "can_manage_topics",
        "can_manage_direct_messages",
        "custom_title"
    )

    def __init__(self, payload: ChatMemberAdministratorPayload):
        super().__init__(payload)
        self.can_be_edited = payload["can_be_edited"]
        self.is_anonymous = payload["is_anonymous"]
        self.can_manage_chat = payload["can_manage_chat"]
        self.can_delete_messages = payload["can_delete_messages"]
        self.can_manage_video_chats = payload["can_manage_video_chats"]
        self.can_restrict_members = payload["can_restrict_members"]
        self.can_promote_members = payload["can_promote_members"]
        self.can_change_info =  payload["can_change_info"]
        self.can_invite_users = payload["can_invite_users"]
        self.can_post_stories = payload["can_post_stories"]
        self.can_edit_stories = payload["can_edit_stories"]
        self.can_delete_stories = payload["can_delete_stories"]
        self.can_post_messages = payload.get("can_post_messages", False)
        self.can_edit_messages = payload.get("can_edit_messages", False)
        self.can_pin_messages = payload.get("can_pin_messages", False)
        self.can_manage_topics = payload.get("can_manage_topics", False)
        self.can_manage_direct_messages = payload.get("can_manage_direct_messages", False)
        self.custom_title = payload.get("custom_title")


class ChatMemberMember(ChatMember):

    __slots__ = (
        "until_date"
    )

    def __init__(self, payload: ChatMemberMemberPayload):
        super().__init__(payload)
        self.until_date = payload.get("until_date", -1)


class ChatMemberRestricted(ChatMember):

    __slots__ = (
        "is_member",
        "can_send_messages",
        "can_send_audios",
        "can_send_documents",
        "can_send_photos",
        "can_send_videos",
        "can_send_video_notes",
        "can_send_voice_notes",
        "can_send_polls",
        "can_send_other_messages",
        "can_add_web_page_reviews",
        "can_change_info",
        "can_invite_users",
        "can_pin_messages",
        "can_manage_topics",
        "until_date"
    )

    def __init__(self, payload: ChatMemberRestrictedPayload):
        super().__init__(payload)
        self.is_member = payload["is_member"]
        self.can_send_messages = payload["can_send_messages"]
        self.can_send_audios = payload["can_send_audios"]
        self.can_send_documents = payload["can_send_documents"]
        self.can_send_photos = payload["can_send_photos"]
        self.can_send_videos = payload["can_send_videos"]
        self.can_send_video_notes = payload["can_send_video_notes"]
        self.can_send_voice_notes = payload["can_send_voice_notes"]
        self.can_send_polls = payload["can_send_polls"]
        self.can_send_other_messages = payload["can_send_other_messages"]
        self.can_add_web_page_reviews = payload["can_add_web_page_reviews"]
        self.can_change_info = payload["can_change_info"]
        self.can_invite_users = payload["can_invite_users"]
        self.can_pin_messages = payload["can_pin_messages"]
        self.can_manage_topics = payload["can_manage_topics"]
        self.until_date = payload["until_date"]


    @property
    def is_restricted_permanently(self):
        return self.until_date == 0


class ChatMemberLeft(ChatMember):
    # Stores no additional data
    def __init__(self, payload: ChatMemberLeftPayload):
        super().__init__(payload)


class ChatMemberBanned(ChatMember):

    __slots__ = (
        "until_date"
    )

    def __init__(self, payload: ChatMemberBannedPayload):
        super().__init__(payload)
        self.until_date = payload["until_date"]  # 0 if permaban

    @property
    def is_banned_permanently(self):
        return self.until_date == 0


class ChatMemberUpdated:

    __slots__ = (
        "chat",
        "from_",
        "date",
        "old_chat_member",
        "new_chat_member",
        "invite_link"
    )

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


class ChatBackground:

    __slots__ = (
        "type"
    )

    def __init__(self, payload: ChatBackgroundPayload):
        self.type = payload["type"]


class VideoChatScheduled:

    __slots__ = (
        "start_date"
    )

    def __init__(self, payload: VideoChatScheduledPayload):
        self.start_date = payload["start_date"]


class VideoChatStarted:
    # Stores no data
    def __init__(self, payload):
        pass


class VideoChatEnded:

    __slots__ = (
        "duration"
    )

    def __init__(self, payload: VideoChatEndedPayload):
        self.duration = payload["duration"]


class VideoChatParticipantsInvited:

    __slots__ = (
        "users"
    )

    def __init__(self, payload: VideoChatParticipantsInvitedPayload):
        self.users = [User(u) for u in payload["users"]]


class Story:

    __slots__ = (
        "chat",
        "id"
    )

    def __init__(self, payload: StoryPayload):
        self.chat = Chat(payload["chat"])
        self.id = payload["id"]
