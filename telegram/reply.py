from typing import List

from .utils import flatten_handlers
from .message_entity import MessageEntity
from .message_properties import MessageOrigin, LinkPreviewOptions
from .checklist import Checklist
from .contact import Contact
from .games import Dice, Game
from .giveaway import Giveaway, GiveawayWinners
from .chat import Chat, Story
from .payments import Invoice
from .location import Location, Venue
from .poll import Poll
from .media import (
    Animation,
    Audio,
    Document,
    PhotoSize,
    Sticker,
    PaidMediaInfo,
    Video,
    VideoNote,
    Voice
)
from .types.reply import (
    ExternalReplyInfo as ExternalReplyInfoPayload,
    TextQuote as TextQuotePayload
)


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


class TextQuote:

    __slots__ = (
        "text",
        "entities",
        "position",
        "is_manual"
    )

    def __init__(self, payload: TextQuotePayload):
        """
        Represents a quoted part in a message that quotes and replies another message.

        :param payload: ``TextQuote`` dictionary received from Telegram API.
        """
        self.text: str = payload["text"]
        """
        Quoted part of the replied message.
        """
        self.entities: List[MessageEntity] = [MessageEntity(e) for e in payload.get("entities", [])]
        """
        List of message entities in the quote.
        """
        self.position = payload["position"]
        """
        Approximate position on the quote in the original message in UTF-16 code units.
        """
        self.is_manual = payload.get("is_manual", False)
        """
        True if the quote was manually selected by user. Otherwise the quote was added by Telegram servers.
        """

    # TODO: Relocate the markdown algorithm to common place where it can be called where applicable
    def markdown(self, make_urls_to_hyperlinks: bool = True) -> str:
        sorted_entities = sorted(self.entities, key=lambda e: e.offset)
        grouped_entities = {}
        for message_entity in sorted_entities:
            grouped_entities.setdefault(message_entity.offset, []).append(message_entity)

        utf16_bytes = bytearray(self.text, "utf-16-le")
        cumulative_offset = 0
        for offset_group in grouped_entities.values():
            entity = offset_group[0]
            entity_start = entity.offset * 2 + cumulative_offset
            entity_end = entity_start + entity.length * 2
            entity_text = utf16_bytes[entity_start:entity_end].decode("utf-16-le")
            markdown, offset = entity.nested_markdown(entity_text, offset_group[1:], make_urls_to_hyperlinks)
            utf16_bytes[entity_start:entity_end] = markdown.encode("utf-16-le")
            cumulative_offset += offset * 2

        return utf16_bytes.decode("utf-16-le")
