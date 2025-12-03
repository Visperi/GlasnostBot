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

from typing import List, Optional, Union

from .utils import flatten_handlers
from .poll import Poll
from .contact import Contact
from .star import StarAmount
from .games import Game, Dice
from .passport import PassportData
from .chat_boost import ChatBoostAdded
from .message_entity import MessageEntity
from .gift import GiftInfo, UniqueGiftInfo
from .user import User, UsersShared, ChatShared
from .reply import TextQuote, ExternalReplyInfo
from .checklist import Checklist, ChecklistTask
from .link_preview_options import LinkPreviewOptions
from .direct_messages_topic import DirectMessagesTopic
from .post import SuggestedPostInfo, SuggestedPostPrice
from .location import Location, Venue, ProximityAlertTriggered
from .payments import SuccessfulPayment, RefundedPayment, Invoice
from .inline import InlineKeyboardMarkup, WebAppData, WriteAccessAllowed
from .message_origin import (
    MessageOrigin,
    MessageOriginUser,
    MessageOriginHiddenUser,
    MessageOriginChat,
    MessageOriginChannel,
)
from .media import (
    MediaBase,
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
from .types.message import (
    MessageAutoDeleteTimerChanged as MessageAutoDeleteTimerChangedPayload,
    SuggestedPostEvent as SuggestedPostEventPayload,
    SuggestedPostApproved as SuggestedPostApprovedPayload,
    SuggestedPostApprovalFailed as SuggestedPostApprovalFailedPayload,
    SuggestedPostDeclined as SuggestedPostDeclinedPayload,
    SuggestedPostPaid as SuggestedPostPaidPayload,
    SuggestedPostRefunded as SuggestedPostRefundedPayload,
    GiveawayCompleted as GiveawayCompletedPayload,
    ChecklistTasksDone as ChecklistTasksDonePayload,
    ChecklistTasksAdded as ChecklistTasksAddedPayload,
    DirectMessagePriceChanged as DirectMessagePriceChangedPayload,
    PaidMessagePriceChanged as PaidMessagePriceChangedPayload,
    MaybeInaccessibleMessage as MaybeInaccessibleMessagePayload,
    InaccessibleMessage as InaccessibleMessagePayload,
    Message as MessagePayload
)


class MessageAutoDeleteTimerChanged:

    __slots__ = "message_auto_delete_time"

    def __init__(self, payload: MessageAutoDeleteTimerChangedPayload):
        self.message_auto_delete_time = payload["message_auto_delete_time"]


class SuggestedPostEvent:

    __slots__ = (
        "suggested_post_message"
    )

    def __init__(self, payload: SuggestedPostEventPayload):
        try:
            self.suggested_post_message = payload.get("suggested_post_message")
        except KeyError:
            self.suggested_post_message = None


class SuggestedPostApproved(SuggestedPostEvent):

    __slots__ = (
        "price",
        "send_date"
    )

    def __init__(self, payload: SuggestedPostApprovedPayload):
        super().__init__(payload)
        self.send_date = payload["send_date"]

        try:
            self.price = SuggestedPostPrice(payload["price"])
        except KeyError:
            self.price = None


class SuggestedPostApprovalFailed(SuggestedPostEvent):

    __slots__ = (
        "price"
    )

    def __init__(self, payload: SuggestedPostApprovalFailedPayload):
        super().__init__(payload)
        self.price = SuggestedPostPrice(payload["price"])


class SuggestedPostDeclined(SuggestedPostEvent):

    __slots__ = (
        "comment"
    )

    def __init__(self, payload: SuggestedPostDeclinedPayload):
        super().__init__(payload)
        self.comment = payload.get("comment")


class SuggestedPostPaid(SuggestedPostEvent):

    __slots__ = (
        "currency",
        "amount",
        "star_amount"
    )

    def __init__(self, payload: SuggestedPostPaidPayload):
        super().__init__(payload)
        self.currency = payload["currency"]
        self.amount = payload.get("amount", -1)

        try:
            self.star_amount = StarAmount(payload["star_amount"])
        except KeyError:
            self.star_amount = None


class SuggestedPostRefunded(SuggestedPostEvent):

    __slots__ = (
        "reason"
    )

    def __init__(self, payload: SuggestedPostRefundedPayload):
        super().__init__(payload)
        self.reason = payload["reason"]


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

    def __init__(self, payload: InaccessibleMessagePayload):
        # TODO: Delete this class if plausible
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
        self.from_: Optional[User] = payload.get("from_")
        self.sender_chat: Optional[Chat] = payload.get("sender_chat")
        self.sender_boost_count = payload.get("sender_boost_count", 0)
        self.sender_business_bot = payload.get("sender_business_bot")
        self.business_connection_id = payload.get("business_connection_id")
        self.forward_origin: Optional[MessageOrigin] = payload.get("forward_origin")
        self.is_topic_message = payload.get("is_topic_message", False)
        self.is_automatic_forward = payload.get("is_automatic_forward", False)
        self.reply_to_message = payload.get("reply_to_message")
        self.external_reply = payload.get("external_reply")
        self.quote: Optional[TextQuote] = payload.get("quote")
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
        self.entities: List[MessageEntity] = payload.get("entities", [])
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
        self.caption_entities = payload.get("caption_entities", [])
        self.show_caption_above_media = payload.get("show_caption_above_media", False)
        self.has_media_spoiler = payload.get("has_media_spoiler", False)
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
        # TODO: This could probably be done better
        origin_type = value["type"]

        if origin_type == "user":
            obj = MessageOriginUser(value)
        elif origin_type == "hidden_user":
            obj = MessageOriginHiddenUser(value)
        elif origin_type == "chat":
            obj = MessageOriginChat(value)
        elif origin_type == "channel":
            obj = MessageOriginChannel(value)
        else:
            raise ValueError(f"Unknown message origin type: {origin_type}")
        self.forward_origin = obj

    def _handle_reply_to_message(self, value):
        self.reply_to_message = Message(value)

    def _handle_external_reply(self, value):
        self.external_reply = ExternalReplyInfo(value)

    def _handle_quote(self, value):
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

    def markdown(self, make_urls_to_hyperlink: bool = True) -> Optional[str]:
        """
        Convert the message and its entities to Markdown.

        :param make_urls_to_hyperlink: Make URLs in text format to hyperlinks with the original text. If a hyperlink
                                       cannot be made, keep them in the original format.
        :return: The message text content in Markdown syntax.
        """
        utf8_text = self.text_content
        if not utf8_text:
            return None

        # Apply markdown to entities from left to right in groups of same offsets, meaning they belong to same text.
        sorted_entities = sorted(self.message_entities, key=lambda e: e.offset)
        grouped_entities = {}
        for message_entity in sorted_entities:
            grouped_entities.setdefault(message_entity.offset, []).append(message_entity)

        utf16_bytes = bytearray(utf8_text, "utf-16-le")
        cumulative_offset = 0  # UTF-16 offset after applying markdown to entities
        for offset_group in grouped_entities.values():
            entity = offset_group[0]
            entity_start = entity.offset * 2 + cumulative_offset
            entity_end = entity_start + entity.length * 2
            entity_text = utf16_bytes[entity_start:entity_end].decode("utf-16-le")
            markdown, offset = entity.nested_markdown(entity_text, offset_group[1:], make_urls_to_hyperlink)
            utf16_bytes[entity_start:entity_end] = markdown.encode("utf-16-le")
            cumulative_offset += offset * 2

        return utf16_bytes.decode("utf-16-le")

    @property
    def sender(self) -> Union[User, Chat]:
        """
        Sender of the message.

        :return: ``telegram.User`` if the message was sent by a user. ``telegram.Chat`` if the message was sent on
                 behalf of a chat or the message was sent to a channel.
        """
        # 'from' field may contain fake data for messages sent on behalf of chat, so need to check this here
        if not self.sender_chat:
            return self.from_
        else:
            return self.sender_chat

    @property
    def original_sender(self) -> Optional[Union[User, str, Chat]]:
        """
        :return: Original sender for a forwarded message. None if the message is not forwarded or contains no
                 forward origin.
        """
        if not self.forward_origin:
            return None
        return self.forward_origin.sender

    @property
    def text_content(self) -> Optional[str]:
        """
        :return: Text content of the message, i.e. text with no media or caption with media. A message cannot have both
                 attributes.
        """
        return self.text or self.caption

    @property
    def message_entities(self) -> List[MessageEntity]:
        """
        :return: List of the message entities, i.e. text entities with no media or caption entities with media. A
                 message cannot have both attributes.
        """
        return self.entities or self.caption_entities

    @property
    def contains_media(self) -> bool:
        """
        :return: True if the message contains any type of media, False otherwise.
        """

        for media_attr in (self.photo,
                            self.document,
                            self.video,
                            self.audio,
                            self.animation,
                            self.video_note,
                            self.voice):
            if media_attr is not None:
                return True

        return False

    def get_all_media(self) -> List[MediaBase]:
        """
        Get all media on the message.

        :return: List of media on the message, or an empty list if it contains no media.
        """
        media_attrs = (self.document,
                       self.video,
                       self.audio,
                       self.animation,
                       self.video_note,
                       self.voice)

        media = []
        if self.photo is not None:
            media.append(self.photo[-1])  # The best quality image available
        for media_attr in media_attrs:
            if media_attr is not None:
                media.append(media_attr)

        return media
