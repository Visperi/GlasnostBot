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


from __future__ import annotations
from typing import List

from typing_extensions import TypedDict, NotRequired, TYPE_CHECKING

from .user import User, UsersShared, WriteAccessAllowed, ChatShared
from .location import Location, Venue, ProximityAlertTriggered
from .contact import Contact
from .reaction import ReactionType, ReactionCount
from .payments import SuccessfulPayment, RefundedPayment, Invoice
from .gift import GiftInfo, UniqueGiftInfo
from .passport import PassportData
from .chat_boost import ChatBoostAdded
from .web_app import WebAppData
from .inline import InlineKeyboardMarkup
from .media import (
    Animation,
    Audio,
    Document,
    PhotoSize,
    Video,
    VideoNote,
    Voice,
    Sticker,
    PaidMediaInfo,
    Story
)
from .forum import (
    ForumTopicCreated,
    ForumTopicClosed,
    ForumTopicEdited,
    ForumTopicReopened,
    GeneralForumTopicHidden,
    GeneralForumTopicUnhidden
)
from .chat import (
    ChatBackground,
    VideoChatStarted,
    VideoChatEnded,
    VideoChatScheduled,
    VideoChatParticipantsInvited
)
from .checklist import (
    Checklist,
    ChecklistTasksDone,
    ChecklistTasksAdded
)
from .giveaway import (
    Giveaway,
    GiveawayWinners,
    GiveawayCreated,
    GiveawayCompleted
)
from .post import (
    SuggestedPostInfo,
    SuggestedPostApproved,
    SuggestedPostApprovalFailed,
    SuggestedPostDeclined,
    SuggestedPostRefunded,
    SuggestedPostPaid
)


if TYPE_CHECKING:
    from .chat import Chat
    from .games import Game, Dice
    from .poll import Poll


class DirectMessagesTopic(TypedDict):
    topic_id: int
    user: NotRequired[User]


class TextQuote(TypedDict):
    text: str
    entities: NotRequired[List[MessageEntity]]
    position: int
    is_manual: NotRequired[bool]


class MessageEntity(TypedDict):
    type: str
    offset: int
    length: int
    url: NotRequired[str]
    user: NotRequired[User]
    language: NotRequired[str]
    custom_emoji_id: NotRequired[str]


class LinkPreviewOptions(TypedDict):
    is_disabled: NotRequired[bool]
    url: NotRequired[str]
    prefer_small_media: NotRequired[bool]
    prefer_large_media: NotRequired[bool]
    show_above_text: NotRequired[bool]


class MessageAutoDeleteTimerChanged(TypedDict):
    message_auto_delete_time: int


class MessageReactionUpdated(TypedDict):
    chat: Chat
    message_id: int
    user: NotRequired[User]
    actor_chat: NotRequired[Chat]
    date: int
    old_reaction: List[ReactionType]
    new_reaction: List[ReactionType]


class MessageReactionCountUpdated(TypedDict):
    chat: Chat
    message_id: int
    date: int
    reactions: List[ReactionCount]


# TODO: Combine/refactor the message origin classes
class MessageOrigin(TypedDict):
    type: str
    date: int


class MessageOriginUser(MessageOrigin):
    sender_user: User


class MessageOriginHiddenUser(MessageOrigin):
    sender_user_name: str


class MessageOriginChat(MessageOrigin):
    sender_chat: Chat
    author_signature: NotRequired[str]


class MessageOriginChannel(MessageOrigin):
    chat: Chat
    message_id: int
    author_signature: NotRequired[str]


class ExternalReplyInfo(TypedDict):
    origin: MessageOrigin
    chat: NotRequired[Chat]
    message_id: NotRequired[int]
    link_preview_options: NotRequired[LinkPreviewOptions]
    animation: NotRequired[Animation]
    audio: NotRequired[Audio]
    document: NotRequired[Document]
    paid_media: NotRequired[PaidMediaInfo]
    photo: NotRequired[List[PhotoSize]]
    sticker: NotRequired[Sticker]
    story: NotRequired[Story]
    video: NotRequired[Video]
    video_note: NotRequired[VideoNote]
    voice: NotRequired[Voice]
    has_media_spoiler: NotRequired[bool]
    checlist: NotRequired[Checklist]
    contact: NotRequired[Contact]
    dice: NotRequired[Dice]
    game: NotRequired[Game]
    giveaway: NotRequired[Giveaway]
    giveaway_winners: NotRequired[GiveawayWinners]
    invoice: NotRequired[Invoice]
    location: NotRequired[Location]
    poll: NotRequired[Poll]
    venue: NotRequired[Venue]


class DirectMessagePriceChanged(TypedDict):
    are_direct_messages_enabled: bool
    direct_message_star_count: int


class PaidMessagePriceChanged(TypedDict):
    paid_message_star_count: int


class MaybeInaccessibleMessage(TypedDict):
    message_id: int
    chat: Chat
    date: int  # Always 0 for inaccessible messages


# TODO: Remove this class and determine the accessibility from the attributes
class InaccessibleMessage(MaybeInaccessibleMessage):
    chat: Chat
    message_id: int
    date: int


class Message(MaybeInaccessibleMessage):
    message_thread_id: NotRequired[int]
    direct_messages_topic: NotRequired[DirectMessagesTopic]
    from_: NotRequired[User]
    sender_chat: NotRequired[Chat]
    sender_boost_count: NotRequired[int]
    sender_business_bot: NotRequired[User]
    business_connection_id: NotRequired[str]
    forward_origin: NotRequired[MessageOrigin]
    is_topic_message: NotRequired[bool]
    is_automatic_forward: NotRequired[bool]
    reply_to_message: NotRequired[Message]
    external_reply: NotRequired[ExternalReplyInfo]
    quote: NotRequired[TextQuote]
    reply_to_story: NotRequired[Story]
    reply_to_checklist_task_id: NotRequired[int]
    via_bot: NotRequired[User]
    edit_date: NotRequired[int]
    has_protected_content: NotRequired[bool]
    is_from_offline: NotRequired[bool]
    is_paid_post: NotRequired[bool]
    media_group_id: NotRequired[str]
    author_signature: NotRequired[str]
    paid_star_count: NotRequired[int]
    text: NotRequired[str]
    entities: NotRequired[List[MessageEntity]]
    link_preview_options: NotRequired[LinkPreviewOptions]
    suggested_post_info: NotRequired[SuggestedPostInfo]
    effect_id: NotRequired[str]
    animation: NotRequired[Animation]
    audio: NotRequired[Audio]
    document: NotRequired[Document]
    paid_media: NotRequired[PaidMediaInfo]
    photo: NotRequired[List[PhotoSize]]
    sticker: NotRequired[Sticker]
    story: NotRequired[Story]
    video: NotRequired[Video]
    video_note: NotRequired[VideoNote]
    voice: NotRequired[Voice]
    caption: NotRequired[str]
    caption_entities: NotRequired[List[MessageEntity]]
    show_caption_above_media: NotRequired[bool]
    has_media_spoiler: NotRequired[bool]
    checklist: NotRequired[Checklist]
    contact: NotRequired[Contact]
    dice: NotRequired[Dice]
    game: NotRequired[Game]
    poll: NotRequired[Poll]
    venue: NotRequired[Venue]
    location: NotRequired[Location]
    new_chat_members: NotRequired[List[User]]
    left_chat_member: NotRequired[User]
    new_chat_title: NotRequired[str]
    new_chat_photo: NotRequired[List[PhotoSize]]
    delete_chat_photo: NotRequired[bool]
    group_chat_created: NotRequired[bool]
    supergroup_chat_created: NotRequired[bool]
    channel_chat_created: NotRequired[bool]
    message_auto_delete_timer_changed: NotRequired[MessageAutoDeleteTimerChanged]
    migrate_to_chat_id: NotRequired[int]
    migrate_from_chat_id: NotRequired[int]
    pinned_message: NotRequired[MaybeInaccessibleMessage]
    invoice: NotRequired[Invoice]
    successful_payment: NotRequired[SuccessfulPayment]
    refunded_payment: NotRequired[RefundedPayment]
    users_shared: NotRequired[UsersShared]
    chat_shared: NotRequired[ChatShared]
    gift: NotRequired[GiftInfo]
    unique_gift: NotRequired[UniqueGiftInfo]
    connected_website: NotRequired[str]
    write_access_allowed: NotRequired[WriteAccessAllowed]
    passport_data: NotRequired[PassportData]
    proximity_alert_triggered: NotRequired[ProximityAlertTriggered]
    boost_added: NotRequired[ChatBoostAdded]
    chat_background_set: NotRequired[ChatBackground]
    checklist_tasks_done: NotRequired[ChecklistTasksDone]
    checklist_tasks_added: NotRequired[ChecklistTasksAdded]
    direct_message_price_changed: NotRequired[DirectMessagePriceChanged]
    forum_topic_created: NotRequired[ForumTopicCreated]
    forum_topic_edited: NotRequired[ForumTopicEdited]
    forum_topic_closed: NotRequired[ForumTopicClosed]
    forum_topic_reopened: NotRequired[ForumTopicReopened]
    general_forum_topic_hidden: NotRequired[GeneralForumTopicHidden]
    general_forum_topic_unhidden: NotRequired[GeneralForumTopicUnhidden]
    giveaway_created: NotRequired[GiveawayCreated]
    giveaway: NotRequired[Giveaway]
    giveaway_winners: NotRequired[GiveawayWinners]
    giveaway_completed: NotRequired[GiveawayCompleted]
    paid_message_price_changed: NotRequired[PaidMessagePriceChanged]
    suggested_post_approved: NotRequired[SuggestedPostApproved]
    suggested_post_approval_failed: NotRequired[SuggestedPostApprovalFailed]
    suggested_post_declined: NotRequired[SuggestedPostDeclined]
    suggested_post_paid: NotRequired[SuggestedPostPaid]
    suggested_post_refunded: NotRequired[SuggestedPostRefunded]
    video_chat_scheduled: NotRequired[VideoChatScheduled]
    video_chat_started: NotRequired[VideoChatStarted]
    video_chat_ended: NotRequired[VideoChatEnded]
    video_chat_participants_invited: NotRequired[VideoChatParticipantsInvited]
    web_app_data: NotRequired[WebAppData]
    reply_markup: NotRequired[InlineKeyboardMarkup]
