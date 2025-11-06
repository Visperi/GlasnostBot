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

from typing import List, Dict

from .utils import flatten_handlers
from .user import User, UsersShared, ChatShared
from .contact import Contact
from .games import Game, Dice
from .location import Location, Venue, ProximityAlertTriggered
from .reaction import ReactionType, ReactionCount
from .payments import SuccessfulPayment, RefundedPayment, Invoice
from .gift import Gift, UniqueGift
from .passport import PassportData
from .chat_boost import ChatBoostAdded
from .inline import InlineKeyboardMarkup, WebAppData, WriteAccessAllowed
from .message_entity import MessageEntity
from .poll import Poll
from .media import (
    PhotoSize,
    Animation,
    Audio,
    Document,
    Video,
    Sticker,
    VideoNote,
    Voice,
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
from .post import (
    SuggestedPostInfo,
    SuggestedPostApproved,
    SuggestedPostApprovalFailed,
    SuggestedPostDeclined,
    SuggestedPostRefunded,
    SuggestedPostPaid
)
from .types.message import (
    Message as MessagePayload,
    MessageAutoDeleteTimerChanged as MessageAutoDeleteTimerChangedPayload,
    MaybeInaccessibleMessage as MaybeInaccessibleMessagePayload,
    MessageOrigin as MessageOriginPayload,
    MessageOriginUser as MessageOriginUserPayload,
    MessageOriginHiddenUser as MessageOriginHiddenUserPayload,
    MessageOriginChat as MessageOriginChatPayload,
    MessageOriginChannel as MessageOriginChannelPayload,
    DirectMessagesTopic as DirectMessagesTopicPayload,
    TextQuote as TextQuotePayload,
    LinkPreviewOptions as LinkPreviewOptionsPayload,
    MessageReactionUpdated as MessageReactionUpdatedPayload,
    MessageReactionCountUpdated as MessageReactionCountUpdatedPayload,
    DirectMessagePriceChanged as DirectMessagePriceChangedPayload,
    PaidMessagePriceChanged as PaidMessagePriceChangedPayload,
    ExternalReplyInfo as ExternalReplyInfoPayload,
    GiftInfoBase as GiftInfoBasePayload,
    GiftInfo as GiftInfoPayload,
    UniqueGiftInfo as UniqueGiftInfoPayload,
    Checklist as ChecklistPayload,
    ChecklistTask as ChecklistTaskPayload,
    ChecklistTasksDone as ChecklistTasksDonePayload,
    ChecklistTasksAdded as ChecklistTasksAddedPayload,
    GiveawayCompleted as GiveawayCompletedPayload
)

# TODO: Refactor some classes out of message modules


class DirectMessagesTopic:

    __slots__ = (
        "topic_id",
        "user"
    )

    def __init__(self, payload: DirectMessagesTopicPayload):
        self.topic_id = payload["topic_id"]

        try:
            self.user = User(payload["user"])
        except KeyError:
            self.user = None


class TextQuote:

    __slots__ = (
        "text",
        "entities",
        "position",
        "is_manual"
    )

    def __init__(self, payload: TextQuotePayload):
        self.text = payload["text"]
        self.entities = payload.get("entities", [])
        self.position = payload["position"]
        self.is_manual = payload.get("is_manual", False)


class LinkPreviewOptions:

    __slots__ = (
        "is_disabled",
        "url",
        "prefer_small_media",
        "prefer_large_media",
        "show_above_text"
    )

    def __init__(self, payload: LinkPreviewOptionsPayload):
        self.is_disabled = payload.get("is_disabled", False)
        self.url = payload.get("url")
        self.prefer_small_media = payload.get("prefer_small_media", False)
        self.prefer_large_media = payload.get("prefer_large_media", False)
        self.show_above_text = payload.get("show_above_text", False)


class MessageAutoDeleteTimerChanged:

    __slots__ = "message_auto_delete_time"

    def __init__(self, payload: MessageAutoDeleteTimerChangedPayload):
        self.message_auto_delete_time = payload["message_auto_delete_time"]


class GiveawayCompleted:

    __slots__ = (
        "winner_count",
        "unclaimed_prize_count",
        "giveaway_message",
        "is_star_giveaway"
    )

    def __init__(self, payload: GiveawayCompletedPayload):
        self.winner_count = payload["winner_count"]
        self.unclaimed_prize_count = payload.get("unclaimed_prize_count", 0)
        self.is_star_giveaway = payload.get("is_star_giveaway", False)

        try:
            self.giveaway_message = Message(payload["giveaway_message"])
        except KeyError:
            self.giveaway_message = None


class ChecklistTask:

    __slots__ = (
        "id",
        "text",
        "text_entities",
        "completed_by_user",
        "completion_date"
    )

    def __init__(self, payload: ChecklistTaskPayload):
        self.id = payload["id"]
        self.text = payload["text"]
        self.text_entities = [MessageEntity(e) for e in payload.get("text_entities", [])]
        self.completion_date = payload.get("completion_date", -1)

        try:
            self.completed_by_user = User(payload["completed_by_user"])
        except KeyError:
            self.completed_by_user = None


class Checklist:

    __slots__ = (
        "title",
        "title_entities",
        "tasks",
        "others_can_add_tasks",
        "others_can_mark_tasks_as_done"
    )

    def __init__(self, payload: ChecklistPayload):
        self.title = payload["title"]
        self.title_entities = [MessageEntity(e) for e in payload.get("title_entities", [])]
        self.tasks = [ChecklistTask(t) for t in payload["tasks"]]
        self.others_can_add_tasks = payload.get("others_can_add_tasks", False)
        self.others_can_mark_tasks_as_done = payload.get("others_can_mark_tasks_as_done", False)


class ChecklistTasksDone:

    __slots__ = (
        "checklist_message",
        "marked_as_done_task_ids",
        "marked_as_not_done_task_ids"
    )

    def __init__(self, payload: ChecklistTasksDonePayload):
        self.marked_as_done_task_ids = payload.get("marked_as_done_task_ids", [])
        self.marked_as_not_done_task_ids = payload.get("marked_as_not_done_task_ids", [])

        try:
            self.checklist_message = Message(payload["checklist_message"])
        except KeyError:
            self.checklist_message = None


class ChecklistTasksAdded:

    __slots__ = (
        "checklist_message",
        "tasks"
    )

    def __init__(self, payload: ChecklistTasksAddedPayload):
        self.tasks = [ChecklistTask(t) for t in payload["tasks"]]

        try:
            self.checklist_message = Message(payload["checklist_message"])
        except KeyError:
            self.checklist_message = None


class MessageReactionUpdated:

    __slots__ = (
        "chat",
        "message_id",
        "user",
        "actor_chat",
        "date",
        "old_reaction",
        "new_reaction"
    )

    def __init__(self, payload: MessageReactionUpdatedPayload):
        self.chat = Chat(payload["chat"])
        self.message_id = payload["message_id"]
        self.date = payload["date"]
        self.old_reaction = [ReactionType(r) for r in payload["old_reaction"]]
        self.new_reaction = [ReactionType(r) for r in payload["new_reaction"]]

        try:
            self.user = User(payload["user"])
        except KeyError:
            self.user = None

        try:
            self.actor_chat = Chat(payload["actor_chat"])
        except KeyError:
            self.actor_chat = None


class MessageReactionCountUpdated:

    __slots__ = (
        "chat",
        "message_id",
        "date",
        "reactions"
    )

    def __init__(self, payload: MessageReactionCountUpdatedPayload):
        self.chat = Chat(payload["chat"])
        self.message_id = payload["message_id"]
        self.date = payload["date"]
        self.reactions = [ReactionCount(r) for r in payload["reactions"]]


# TODO: Move message origin classes to module message_origin
class MessageOrigin:

    __slots__ = (
        "type",
        "date"
    )

    def __init__(self, payload: MessageOriginPayload):
        self.type = payload["type"]
        self.date = payload["date"]


class MessageOriginUser(MessageOrigin):

    __slots__ = (
        "sender_user"
    )

    def __init__(self, payload: MessageOriginUserPayload):
        super().__init__(payload)
        self.sender_user = User(payload["sender_user"])


class MessageOriginHiddenUser(MessageOrigin):

    __slots__ = (
        "sender_user_name"
    )

    def __init__(self, payload: MessageOriginHiddenUserPayload):
        super().__init__(payload)
        self.sender_user_name = payload["sender_user_name"]


class MessageOriginChat(MessageOrigin):

    __slots__ = (
        "sender_chat",
        "author_signature"
    )

    def __init__(self, payload: MessageOriginChatPayload):
        super().__init__(payload)
        self.sender_chat = Chat(payload["sender_chat"])
        self.author_signature = payload.get("author_signature")


class MessageOriginChannel(MessageOrigin):

    __slots__ = (
        "chat",
        "message_id",
        "author_signature"
    )

    def __init__(self, payload: MessageOriginChannelPayload):
        super().__init__(payload)
        self.chat = Chat(payload["chat"])
        self.message_id = payload["message_id"]
        self.author_signature = payload.get("author_signature")


# TODO: Combine with Message
@flatten_handlers
class ExternalReplyInfo:
    _HANDLERS = []

    __slots__ = (
        "origin",
        "chat",
        "message_id",
        "link_preview_options",
        "animation",
        "audio",
        "document",
        "paid_media",
        "photo",
        "sticker",
        "story",
        "video",
        "video_note",
        "voice",
        "has_media_spoiler",
        "checklist",
        "contact",
        "dice",
        "game",
        "giveaway",
        "giveaway_winners",
        "invoice",
        "location",
        "poll",
        "venue"
    )

    def __init__(self, payload: ExternalReplyInfoPayload):
        self.origin = MessageOrigin(payload["origin"])
        self.chat = payload.get("chat")
        self.message_id = payload.get("message_id", -1)
        self.link_preview_options = payload.get("link_preview_options")
        self.animation = payload.get("animation")
        self.audio = payload.get("audio")
        self.document = payload.get("document")
        self.paid_media = payload.get("paid_media")
        self.photo = payload.get("photo")
        self.sticker = payload.get("sticker")
        self.story = payload.get("story")
        self.video = payload.get("video")
        self.video_note = payload.get("video_note")
        self.voice = payload.get("voice")
        self.has_media_spoiler = payload.get("has_media_spoiler", False)
        self.checklist = payload.get("checklist")
        self.contact = payload.get("contact")
        self.dice = payload.get("dice")
        self.game = payload.get("game")
        self.giveaway = payload.get("giveaway")
        self.giveaway_winners = payload.get("giveaway_winners")
        self.invoice = payload.get("invoice")
        self.location = payload.get("location")
        self.poll = payload.get("poll")
        self.venue = payload.get("venue")

        for key, func in self._HANDLERS:
            try:
                value = payload[key]  # type: ignore
            except KeyError:
                continue
            else:
                func(self, value)

    def _handle_chat(self, value):
        self.chat = Chat(value)

    def _handle_link_preview_options(self, value):
        self.link_preview_options = LinkPreviewOptions(value)

    def _handle_animation(self, value):
        self.animation = Animation(value)

    def _handle_audio(self, value):
        self.animation = Audio(value)

    def _handle_document(self, value):
        self.document = Document(value)

    def _handle_paid_media(self, value):
        self.paid_media = PaidMediaInfo(value)

    def _handle_photo(self, value):
        self.photo = [PhotoSize(p) for p in value]

    def _handle_sticker(self, value):
        self.sticker = Sticker(value)

    def _handle_story(self, value):
        self.story = Story(value)

    def _handle_video(self, value):
        self.video = Video(value)

    def _handle_video_note(self, value):
        self.video_note = VideoNote(value)

    def _handle_voice(self, value):
        self.video_note = Voice(value)

    def _handle_checklist(self, value):
        self.checklist = Checklist(value)

    def _handle_contact(self, value):
        self.contact = Contact(value)

    def _handle_dice(self, value):
        self.dice = Dice(value)

    def _handle_game(self, value):
        self.game = Game(value)

    def _handle_giveaway(self, value):
        self.giveaway = Giveaway(value)

    def _handle_giveaway_winners(self, value):
        self.giveaway_winners = GiveawayWinners(value)

    def _handle_invoice(self, value):
        self.invoice = Invoice(value)

    def _handle_location(self, value):
        self.location = Location(value)

    def _handle_poll(self, value):
        self.poll = Poll(value)

    def _handle_venue(self, value):
        self.venue = Venue(value)


class DirectMessagePriceChanged:

    __slots__ = (
        "are_direct_messages_enabled",
        "direct_message_star_count"
    )

    def __init__(self, payload: DirectMessagePriceChangedPayload):
        self.are_direct_messages_enabled = payload["are_direct_messages_enabled"]
        self.direct_message_star_count = payload["direct_message_star_count"]


class PaidMessagePriceChanged:

    __slots__ = (
        "paid_message_star_count"
    )

    def __init__(self, payload: PaidMessagePriceChangedPayload):
        self.paid_message_star_count = payload["paid_message_star_count"]


class GiftInfoBase:

    __slots__ = (
        "owned_gift_id"
    )

    def __init__(self, payload: GiftInfoBasePayload):
        self.owned_gift_id = payload.get("owned_gift_id")


class GiftInfo(GiftInfoBase):

    __slots__ = (
        "gift",
        "convert_star_count",
        "prepaid_upgrade_star_count",
        "can_be_upgraded",
        "text",
        "entities",
        "is_private"
    )

    def __init__(self, payload: GiftInfoPayload):
        super().__init__(payload)
        self.gift = Gift(payload["gift"])
        self.convert_star_count = payload.get("convert_star_count", 0)
        self.prepaid_upgrade_star_count = payload.get("prepaid_upgrade_star_count", 0)
        self.can_be_upgraded = payload.get("can_be_upgraded", False)
        self.text = payload.get("text")
        self.entities = [MessageEntity(e) for e in payload.get("entities", [])]
        self.is_private = payload.get("is_private", False)


class UniqueGiftInfo(GiftInfoBase):

    __slots__ = (
        "gift",
        "origin",
        "last_resale_star_count",
        "transfer_star_count",
        "next_transfer_date"
    )

    def __init__(self, payload: UniqueGiftInfoPayload):
        super().__init__(payload)
        self.gift = UniqueGift(payload["gift"])
        self.origin = payload["origin"]
        self.last_resale_star_count = payload.get("last_resale_star_count")
        self.transfer_star_count = payload.get("transfer_star_count", 0)
        self.next_transfer_date = payload.get("next_transfer_date", -1)


class MaybeInaccessibleMessage:

    __slots__ = (
        "message_id",
        "chat",
        "date"
    )

    def __init__(self, payload: MaybeInaccessibleMessagePayload):
        self.message_id = payload["message_id"]
        self.chat = Chat(payload["chat"])
        self.date = payload["date"]  # 0 for inaccessible messages


class InaccessibleMessage(MaybeInaccessibleMessage):

    def __init__(self, payload):
        # TODO: Delete this class is plausible
        super().__init__(payload)


@flatten_handlers
class Message(MaybeInaccessibleMessage):
    _HANDLERS = []

    __slots__ = (
        "message_thread_id",
        "direct_messages_topic",
        "from_",
        "sender_chat",
        "sender_boost_count",
        "sender_business_bot",
        "business_connection_id",
        "forward_origin",
        "is_topic_message",
        "is_automatic_forward",
        "reply_to_message",
        "external_reply",
        "quote",
        "reply_to_story",
        "reply_to_checklist_task_id",
        "via_bot",
        "edit_date",
        "has_protected_content",
        "is_from_offline",
        "is_paid_post",
        "media_group_id",
        "author_signature",
        "paid_star_count",
        "text",
        "entities",
        "link_preview_options",
        "suggested_post_info",
        "effect_id",
        "animation",
        "audio",
        "document",
        "paid_media",
        "photo",
        "sticker",
        "story",
        "video",
        "video_note",
        "voice",
        "caption",
        "caption_entities",
        "show_caption_above_media",
        "has_media_spoiler",
        "checklist",
        "contact",
        "dice",
        "game",
        "poll",
        "venue",
        "location",
        "new_chat_members",
        "left_chat_member",
        "new_chat_title",
        "new_chat_photo",
        "delete_chat_photo",
        "group_chat_created",
        "supergroup_chat_created",
        "channel_chat_created",
        "message_auto_delete_timer_changed",
        "migrate_to_chat_id",
        "migrate_from_chat_id",
        "pinned_message",
        "invoice",
        "successful_payment",
        "refunded_payment",
        "users_shared",
        "chat_shared",
        "gift",
        "unique_gift",
        "connected_website",
        "write_access_allowed",
        "passport_data",
        "proximity_alert_triggered",
        "boost_added",
        "chat_background_set",
        "checklist_tasks_done",
        "checklist_tasks_added",
        "direct_message_price_changed",
        "forum_topic_created",
        "forum_topic_edited",
        "forum_topic_closed",
        "forum_topic_reopened",
        "general_forum_topic_hidden",
        "general_forum_topic_unhidden",
        "giveaway_created",
        "giveaway",
        "giveaway_winners",
        "giveaway_completed",
        "paid_message_price_changed",
        "suggested_post_approved",
        "suggested_post_approval_failed",
        "suggested_post_declined",
        "suggested_post_paid",
        "suggested_post_refunded",
        "video_chat_scheduled",
        "video_chat_started",
        "video_chat_ended",
        "video_chat_participants_invited",
        "web_app_data",
        "reply_markup"
    )

    def __init__(self, payload: MessagePayload) -> None:
        super().__init__(payload)

        self.message_thread_id = payload.get("message_thread_id", -1)
        self.direct_messages_topic = payload.get("direct_messages_topic")
        self.from_ = payload.get("from_")
        self.sender_chat = payload.get("sender_chat")
        self.sender_boost_count = payload.get("sender_boost_count", 0)
        self.sender_business_bot = payload.get("sender_business_bot")
        self.business_connection_id = payload.get("business_connection_id")
        self.forward_origin = payload.get("forward_origin")
        self.is_topic_message = payload.get("is_topic_message", False)
        self.is_automatic_forward = payload.get("is_automatic_forward", False)
        self.reply_to_message = payload.get("reply_to_message")
        self.external_reply = payload.get("external_reply")
        self.quote = payload.get("quote")
        self.reply_to_story = payload.get("reply_to_story")
        self.reply_to_checklist_task_id = payload.get("reply_to_checklist_task_id", -1)
        self.via_bot = payload.get("via_bot")
        self.edit_date = payload.get("edit_date", -1)
        self.has_protected_content = payload.get("has_protected_content", False)
        self.is_from_offline = payload.get("is_from_offline", False)
        self.is_paid_post = payload.get("is_paid_post", False)
        self.media_group_id = payload.get("media_group_id")
        self.author_signature = payload.get("author_signature")
        self.paid_star_count = payload.get("paid_star_count", 0)
        self.text = payload.get("text")
        self.entities = payload.get("entities")
        self.link_preview_options = payload.get("link_preview_options")
        self.suggested_post_info = payload.get("suggested_post_info")
        self.effect_id = payload.get("effect_id")
        self.animation = payload.get("animation")
        self.audio = payload.get("audio")
        self.document = payload.get("document")
        self.paid_media = payload.get("paid_media")
        self.photo = payload.get("photo")
        self.sticker = payload.get("sticker")
        self.story = payload.get("story")
        self.video = payload.get("video")
        self.video_note = payload.get("video_note")
        self.voice = payload.get("voice")
        self.caption = payload.get("caption")
        self.caption_entities = payload.get("caption_entities")
        self.show_caption_above_media = payload.get("show_caption_above_media", False)
        self.has_media_spoiler = payload.get("has_media_spoiler")
        self.checklist = payload.get("checklist")
        self.contact = payload.get("contact")
        self.dice = payload.get("dice")
        self.game = payload.get("game")
        self.poll = payload.get("poll")
        self.venue = payload.get("venue")
        self.location = payload.get("location")
        self.new_chat_members = payload.get("new_chat_members")
        self.left_chat_member = payload.get("left_chat_member")
        self.new_chat_title = payload.get("new_chat_title")
        self.new_chat_photo = payload.get("new_chat_photo")
        self.delete_chat_photo = payload.get("delete_chat_photo", False)
        self.group_chat_created = payload.get("group_chat_created", False)
        self.supergroup_chat_created = payload.get("supergroup_chat_created", False)
        self.channel_chat_created = payload.get("channel_chat_created", False)
        self.message_auto_delete_timer_changed = payload.get("message_auto_delete_timer_changed")
        self.migrate_to_chat_id = payload.get("migrate_to_chat_id", -1)
        self.migrate_from_chat_id = payload.get("migrate_from_chat_id", -1)
        self.pinned_message = payload.get("pinned_message")
        self.invoice = payload.get("invoice")
        self.successful_payment = payload.get("successful_payment")
        self.refunded_payment = payload.get("refunded_payment")
        self.users_shared = payload.get("users_shared")
        self.chat_shared = payload.get("chat_shared")
        self.gift = payload.get("gift")
        self.unique_gift = payload.get("unique_gift")
        self.connected_website = payload.get("connected_website")
        self.write_access_allowed = payload.get("write_access_allowed")
        self.passport_data = payload.get("passport_data")
        self.proximity_alert_triggered = payload.get("proximity_alert_triggered")
        self.boost_added = payload.get("boost_added")
        self.chat_background_set = payload.get("chat_background_set")
        self.checklist_tasks_done = payload.get("checklist_tasks_done")
        self.checklist_tasks_added = payload.get("checklist_tasks_added")
        self.direct_message_price_changed = payload.get("direct_message_price_changed")
        self.forum_topic_created = payload.get("forum_topic_created")
        self.forum_topic_edited = payload.get("forum_topic_edited")
        self.forum_topic_closed = payload.get("forum_topic_closed")
        self.forum_topic_reopened = payload.get("forum_topic_reopened")
        self.general_forum_topic_hidden = payload.get("general_forum_topic_hidden")
        self.general_forum_topic_unhidden = payload.get("general_forum_topic_unhidden")
        self.giveaway_created = payload.get("giveaway_created")
        self.giveaway = payload.get("giveaway")
        self.giveaway_winners = payload.get("giveaway_winners")
        self.giveaway_completed = payload.get("giveaway_completed")
        self.paid_message_price_changed = payload.get("paid_message_price_changed")
        self.suggested_post_approved = payload.get("suggested_post_approved")
        self.suggested_post_approval_failed = payload.get("suggested_post_approval_failed")
        self.suggested_post_declined = payload.get("suggested_post_declined")
        self.suggested_post_paid = payload.get("suggested_post_paid")
        self.suggested_post_refunded = payload.get("suggested_post_refunded")
        self.video_chat_scheduled = payload.get("video_chat_scheduled")
        self.video_chat_started = payload.get("video_chat_started")
        self.video_chat_ended = payload.get("video_chat_ended")
        self.video_chat_participants_invited = payload.get("video_chat_participants_invited")
        self.web_app_data =payload.get("web_app_data")
        self.reply_markup = payload.get("reply_markup")

        for key, func in self._HANDLERS:
            try:
                value = payload[key]  # type: ignore
            except KeyError:
                continue
            else:
                func(self, value)

    def _handle_direct_messages_topic(self, value):
        self.direct_messages_topic = DirectMessagesTopic(value)

    def _handle_from_(self, value):
        self.from_ = User(value)

    def _handle_sender_chat(self, value):
        self.sender_chat = Chat(value)

    def _handle_sender_business_bot(self, value):
        self.sender_business_bot = User(value)

    def _handle_forward_origin(self, value):
        self.forward_origin = MessageOrigin(value)

    def _handle_reply_to_message(self, value):
        self.reply_to_message = Message(value)

    def _handle_external_reply(self, value):
        self.external_reply = ExternalReplyInfo(value)

    def _handle_quote_(self, value):
        self.quote = TextQuote(value)

    def _handle_reply_to_story(self, value):
        self.reply_to_story = Story(value)

    def _handle_via_bot(self, value):
        self.via_bot = User(value)

    def _handle_entities(self, value):
        self.entities = [MessageEntity(e) for e in value]

    def _handle_link_preview_options(self, value):
        self.link_preview_options = LinkPreviewOptions(value)

    def _handle_suggested_post_info(self, value):
        self.suggested_post_info = SuggestedPostInfo(value)

    def _handle_animation(self, value):
        self.animation = Animation(value)

    def _handle_audio(self, value):
        self.audio = Audio(value)

    def _handle_document(self, value):
        self.document = Document(value)

    def _handle_paid_media(self, value):
        self.paid_media = PaidMediaInfo(value)

    def _handle_photo(self, value):
        self.photo = [PhotoSize(p) for p in value]

    def _handle_sticker(self, value):
        self.sticker = Sticker(value)

    def _handle_story(self, value):
        self.story = Story(value)

    def _handle_video(self, value):
        self.video = Video(value)

    def _handle_video_note(self, value):
        self.video_note = VideoNote(value)

    def _handle_voice(self, value):
        self.voice = Voice(value)

    def _handle_caption_entities(self, value):
        self.caption_entities = [MessageEntity(e) for e in value]

    def _handle_checklist(self, value):
        self.checklist = Checklist(value)

    def _handle_contact(self, value):
        self.contact = Contact(value)

    def _handle_dice(self, value):
        self.dice = Dice(value)

    def _handle_game(self, value):
        self.game = Game(value)

    def _handle_poll(self, value):
        self.poll = Poll(value)

    def _handle_venue(self, value):
        self.venue = Venue(value)

    def _handle_location(self, value):
        self.location = Location(value)

    def _handle_new_chat_members(self, value):
        self.new_chat_members = [User(u) for u in value]

    def _handle_left_chat_member(self, value):
        self.left_chat_member = User(value)

    def _handle_new_chat_photo(self, value):
        self.new_chat_photo = [PhotoSize(p) for p in value]

    def _handle_message_auto_delete_timer_changed(self, value):
        self.message_auto_delete_timer_changed = MessageAutoDeleteTimerChanged(value)

    def _handle_pinned_message(self, value):
        self.pinned_message = Message(value)

    def _handle_invoice(self, value):
        self.invoice = Invoice(value)

    def _handle_successful_payment(self, value):
        self.successful_payment = SuccessfulPayment(value)

    def _handle_refunded_payment(self, value):
        self.refunded_payment = RefundedPayment(value)

    def _handle_users_shared(self, value):
        self.users_shared = UsersShared(value)

    def _handle_chat_shared(self, value):
        self.chat_shared = ChatShared(value)

    def _handle_gift(self, value):
        self.gift = GiftInfo(value)

    def _handle_unique_gift(self, value):
        self.unique_gift = UniqueGiftInfo(value)

    def _handle_write_access_allowed(self, value):
        self.write_access_allowed = WriteAccessAllowed(value)

    def _handle_passport_data(self, value):
        self.passport_data = PassportData(value)

    def _handle_proximity_alert_triggered(self, value):
        self.proximity_alert_triggered = ProximityAlertTriggered(value)

    def _handle_boost_added(self, value):
        self.boost_added = ChatBoostAdded(value)

    def _handle_chat_background_set(self, value):
        self.chat_background_set = ChatBackground(value)

    def _handle_checklist_tasks_done(self, value):
        self.checklist_tasks_done = ChecklistTasksDone(value)

    def _handle_checklist_tasks_added(self, value):
        self.checklist_tasks_added = ChecklistTasksAdded(value)

    def _handle_direct_message_price_changed(self, value):
        self.direct_message_price_changed = DirectMessagePriceChanged(value)

    def _handle_forum_topic_created(self, value):
        self.forum_topic_created = ForumTopicCreated(value)

    def _handle_forum_topic_edited(self, value):
        self.forum_topic_edited = ForumTopicEdited(value)

    def _handle_forum_topic_closed(self, value):
        self.forum_topic_closed = ForumTopicClosed(value)

    def _handle_forum_topic_reopened(self, value):
        self.forum_topic_reopened = ForumTopicReopened(value)

    def _handle_general_forum_topic_hidden(self, value):
        self.general_forum_topic_hidden = GeneralForumTopicHidden(value)

    def _handle_general_forum_topic_unhidden(self, value):
        self.general_forum_topic_unhidden = GeneralForumTopicUnhidden(value)

    def _handle_giveaway_created(self, value):
        self.giveaway_created = GiveawayCreated(value)

    def _handle_giveaway(self, value):
        self.giveaway = Giveaway(value)

    def _handle_giveaway_winners(self, value):
        self.giveaway_winners = GiveawayWinners(value)

    def _handle_giveaway_completed(self, value):
        self.giveaway_completed = GiveawayCompleted(value)

    def _handle_paid_message_price_changed(self, value):
        self.paid_message_price_changed = PaidMessagePriceChanged(value)

    def _handle_suggested_post_approved(self, value):
        self.suggested_post_approved = SuggestedPostApproved(value)

    def _handle_suggested_post_approval_failed(self, value):
        self.suggested_post_approval_failed = SuggestedPostApprovalFailed(value)

    def _handle_suggested_post_declined(self, value):
        self.suggested_post_declined = SuggestedPostDeclined(value)

    def _handle_suggested_post_paid(self, value):
        self.suggested_post_paid = SuggestedPostPaid(value)

    def _handle_suggested_post_refunded(self, value):
        self.suggested_post_refunded = SuggestedPostRefunded(value)

    def _handle_video_chat_scheduled(self, value):
        self.video_chat_scheduled = VideoChatScheduled(value)

    def _handle_video_chat_started(self, value):
        self.video_chat_started = VideoChatStarted(value)

    def _handle_video_chat_ended(self, value):
        self.video_chat_ended = VideoChatEnded(value)

    def _handle_video_chat_participants_invited(self, value):
        self.video_chat_participants_invited = VideoChatParticipantsInvited(value)

    def _handle_web_app_data(self, value):
        self.web_app_data = WebAppData(value)

    def _handle_reply_markup(self, value):
        self.reply_markup = InlineKeyboardMarkup(value)

    @property
    def text_formatted(self) -> str:
        """
        Telegram message content and entities combined into Markdown syntax. Uses markdownify method with default
        settings, so use that method instead if more control is needed.
        """
        return self.markdownify()

    def _group_entities(self) -> Dict[int, List[MessageEntity]]:
        """
        Group message entities with same offsets together.

        :return: Dictionary containing offsets as keys and list of entities with the offset.
        """
        grouped_entities = {}
        for entity in self.entities:
            try:
                grouped_entities[entity.offset].append(entity)
            except KeyError:
                grouped_entities[entity.offset] = [entity]

        return grouped_entities

    def markdownify(self, make_urls_to_hyperlink: bool = True) -> str:
        """
        Apply message entities in Markdown syntax to the message content.

        :return: Message content with entities added in Markdown syntax.
        """
        markdownified = self.text
        grouped_entities = self._group_entities()
        total_offset = 0

        # TODO: Use this to fix the codepoint issues
        # https://stackoverflow.com/questions/39280183/utf-16-codepoint-counting-in-python
        text_utf16 = self.text.encode("utf-16-le")

        for offset_entities in grouped_entities.values():
            one_way_offset = total_offset  # Offset needed in nested entities
            for entity in offset_entities:
                offset = entity.offset + one_way_offset
                entity_end = offset + entity.length
                text_seq = markdownified[offset:entity_end]
                entity_markdown = entity.markdown(text_seq, make_urls_to_hyperlink)
                markdownified = markdownified[:offset] + entity_markdown + markdownified[offset+entity.length:]

                one_way_offset += entity.one_way_markdown_offset
                total_offset += len(entity_markdown) - len(text_seq)

        return markdownified
