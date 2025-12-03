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


from typing import TypedDict, NotRequired, List

from .user import User
from .background import BackgroundType


class ChatPhoto(TypedDict):
    small_file_id: str
    small_file_unique_id: str
    big_file_id: str
    big_file_unique_id: str


class ChatPermissions(TypedDict):
    can_send_messages: NotRequired[bool]
    can_send_audios: NotRequired[bool]
    can_send_documents: NotRequired[bool]
    can_send_photos: NotRequired[bool]
    can_send_videos: NotRequired[bool]
    can_send_video_notes: NotRequired[bool]
    can_send_voice_notes: NotRequired[bool]
    can_send_polls: NotRequired[bool]
    can_send_other_messages: NotRequired[bool]
    can_add_web_page_previews: NotRequired[bool]
    can_change_info: NotRequired[bool]
    can_invite_users: NotRequired[bool]
    can_pin_messages: NotRequired[bool]
    can_manage_topics: NotRequired[bool]


class Chat(TypedDict):
    id: int
    type: str
    title: NotRequired[str]
    username: NotRequired[str]
    first_name: NotRequired[str]
    last_name: NotRequired[str]
    is_forum: NotRequired[bool]
    is_direct_messages: NotRequired[bool]


class ChatInviteLink(TypedDict):
    invite_link: str
    creator: User
    creates_join_request: bool
    is_primary: bool
    is_revoked: bool
    name: NotRequired[str]
    expire_date: NotRequired[int]
    member_limit: NotRequired[int]
    pending_join_request_count: NotRequired[int]
    subscription_period: NotRequired[int]
    subscription_price: NotRequired[int]


class ChatJoinRequest(TypedDict):
    chat: Chat
    from_: User
    user_chat_id: int
    date: int
    bio: NotRequired[str]
    invite_link: NotRequired[ChatInviteLink]


class ChatMember(TypedDict):
    status: str
    user: User


# TODO: Combine below Member classes if possible
class ChatMemberOwner(ChatMember):
    is_anonymous: bool
    custom_title: NotRequired[str]


class ChatMemberAdministrator(ChatMember):
    can_be_edited: bool
    is_anonymous: bool
    can_manage_chat: bool
    can_delete_messages: bool
    can_manage_video_chats: bool
    can_restrict_members: bool
    can_promote_members: bool
    can_change_info: bool
    can_invite_users: bool
    can_post_stories: bool
    can_edit_stories: bool
    can_delete_stories: bool
    can_post_messages: NotRequired[bool]
    can_edit_messages: NotRequired[bool]
    can_pin_messages: NotRequired[bool]
    can_manage_topics: NotRequired[bool]
    can_manage_direct_messages: NotRequired[bool]
    custom_title: NotRequired[str]


class ChatMemberMember(ChatMember):
    until_date: NotRequired[int]


class ChatMemberRestricted(ChatMember):
    is_member: bool
    can_send_messages: bool
    can_send_audios: bool
    can_send_documents: bool
    can_send_photos: bool
    can_send_videos: bool
    can_send_video_notes: bool
    can_send_voice_notes: bool
    can_send_polls: bool
    can_send_other_messages: bool
    can_add_web_page_reviews: bool
    can_change_info: bool
    can_invite_users: bool
    can_pin_messages: bool
    can_manage_topics: bool
    until_date: int  # 0 if restricted forever


class ChatMemberLeft(ChatMember):
    pass  # Stores no data


class ChatMemerBanned(ChatMember):
    until_date: int  # 0 if permaban


class ChatMemberUpdated(TypedDict):
    chat: Chat
    from_: User
    date: int
    old_chat_member: ChatMember
    new_chat_member: ChatMember
    invite_link: NotRequired[ChatInviteLink]


class ChatBackground(TypedDict):
    type: BackgroundType


class VideoChatScheduled(TypedDict):
    start_date: int


class VideoChatStarted(TypedDict):
    # Stores no data
    pass


class VideoChatEnded(TypedDict):
    duration: int


class VideoChatParticipantsInvited(TypedDict):
    users: List[User]


class Story(TypedDict):
    chat: Chat
    id: int
