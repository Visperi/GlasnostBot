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

from __future__ import annotations


from typing import TypedDict, NotRequired, List

from .poll import Poll
from .contact import Contact
from .star import StarAmount
from .reply import TextQuote
from .games import Game, Dice
from .passport import PassportData
from .chat_boost import ChatBoostAdded
from .message_entity import MessageEntity
from .gift import GiftInfo, UniqueGiftInfo
from .user import User, UsersShared, ChatShared
from .checklist import Checklist, ChecklistTask
from .post import SuggestedPostInfo, SuggestedPostPrice
from .location import Location, Venue, ProximityAlertTriggered
from .payments import SuccessfulPayment, RefundedPayment, Invoice
from .inline import InlineKeyboardMarkup, WebAppData, WriteAccessAllowed
from .message_properties import (
    MessageOrigin,
    LinkPreviewOptions,
    DirectMessagesTopic
)
from .media import (
    Animation,
    Audio,
    Document,
    PhotoSize,
    Video,
    VideoNote,
    Voice,
    Sticker,
    PaidMediaInfo
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
    Chat,
    Story,
    ChatBackground,
    VideoChatStarted,
    VideoChatEnded,
    VideoChatScheduled,
    VideoChatParticipantsInvited
)
from .giveaway import (
    Giveaway,
    GiveawayWinners,
    GiveawayCreated
)


class MessageAutoDeleteTimerChanged(TypedDict):
    message_auto_delete_time: int


class SuggestedPostEvent(TypedDict):
    suggested_post_message: NotRequired[Message]


class SuggestedPostApproved(SuggestedPostEvent):
    price: NotRequired[SuggestedPostPrice]
    send_date: int


class SuggestedPostApprovalFailed(SuggestedPostEvent):
    price: SuggestedPostPrice


class SuggestedPostDeclined(SuggestedPostEvent):
    comment: NotRequired[str]


class SuggestedPostPaid(SuggestedPostEvent):
    currency: str
    amount: NotRequired[int]
    star_amount: NotRequired[StarAmount]


class SuggestedPostRefunded(SuggestedPostEvent):
    reason: str


class GiveawayCompleted(TypedDict):
    winner_count: int
    unclaimed_prize_count: NotRequired[int]
    giveaway_message: NotRequired[Message]
    is_star_giveaway: NotRequired[bool]


class ChecklistTasksDone(TypedDict):
    checklist_message: NotRequired[Message]
    marked_as_done_task_ids: NotRequired[List[int]]
    marked_as_not_done_task_ids: NotRequired[List[int]]


class ChecklistTasksAdded(TypedDict):
    checklist_message: NotRequired[Message]
    tasks: List[ChecklistTask]


class DirectMessagePriceChanged(TypedDict):
    are_direct_messages_enabled: bool
    direct_message_star_count: int


class PaidMessagePriceChanged(TypedDict):
    paid_message_star_count: int


# TODO: Combine with Message
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
    checklist: NotRequired[Checklist]
    contact: NotRequired[Contact]
    dice: NotRequired[Dice]
    game: NotRequired[Game]
    giveaway: NotRequired[Giveaway]
    giveaway_winners: NotRequired[GiveawayWinners]
    invoice: NotRequired[Invoice]
    location: NotRequired[Location]
    poll: NotRequired[Poll]
    venue: NotRequired[Venue]


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
