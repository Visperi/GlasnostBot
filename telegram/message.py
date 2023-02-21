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

from .chat import Chat
from .user import User
from .contact import Contact
from .poll import Poll
from .game import Game, Dice
from .location import Location, Venue
from .document import (
    PhotoSize,
    Animation,
    Audio,
    Document,
    Video,
    Sticker,
    VideoNote,
    Voice
)
from .types.message import (
    Message as MessagePayload,
    MessageEntity as MessageEntityPayload,
    MessageAutoDeleteTimerChanged as MessageAutoDeleteTimerChangedPayload
)
from .utils import flatten_handlers
from typing import Optional, List, Dict
from urllib.parse import urlparse, urlunparse


class EntityType:

    Bold = "bold"
    Italic = "italic"
    Underline = "underline"
    Strikethrough = "strikethrough"
    Spoiler = "spoiler"
    Code = "code"
    Codeblock = "pre"
    Mention = "mention"
    Hashtag = "hashtag"
    Cashtag = "cashtag"
    BotCommand = "bot_command"
    Url = "url"
    Email = "email"
    PhoneNumber = "phone_number"
    TextLink = "text_link"
    TextMention = "text_mention"
    CustomEmoji = "custom_emoji"

    @classmethod
    def supports_markdown(cls, entity_type: str) -> bool:
        return entity_type not in [
            cls.Mention,
            cls.Hashtag,
            cls.Cashtag,
            cls.BotCommand,
            cls.Email,
            cls.PhoneNumber,
            cls.TextMention,
            cls.CustomEmoji
        ]


class MessageEntity:

    __slots__ = (
        "type",
        "offset",
        "length",
        "url",
        "user",
        "language",
        "custom_emoji_id"
    )

    def __init__(self, payload: MessageEntityPayload):
        self._update(payload)

    def _update(self, payload: MessageEntityPayload):
        self.type = payload["type"]
        self.offset = payload["offset"]
        self.length = payload["length"]
        self.url = payload.get("url")
        self.user = payload.get("user")
        self.language = payload.get("language")
        self.custom_emoji_id = payload.get("custom_emoji_id")

    @staticmethod
    def _complete_url(url: str) -> str:
        """
        Complete partial url so that it has scheme and starts with www. Does nothing for already complete urls.

        :param url: Url to be completed
        :return: Completed url including scheme and starting with www.
        """
        tmp = urlparse(url, "http")
        netloc = tmp.netloc or tmp.path
        path = tmp.path if tmp.netloc else ""

        filled = tmp._replace(netloc=netloc, path=path)
        return urlunparse(filled)

    @staticmethod
    def _make_hyperlink(text: str, url: str) -> str:
        """
        Convert bare text to a hyperlink.

        :param text: Hyperlink text
        :param url: Hyperlink url
        :return: Hyperlink with given text and url
        """
        return f"[{text}]({url})"

    def markdown(self, text: str) -> Optional[str]:
        """
        Convert entity to Markdown syntax with given text.

        :param text: Content for the Markdown conversion.
        :return: Given text converted to Entity Markdown syntax
        """

        if self.type == EntityType.Bold:
            return f"**{text}**"
        elif self.type == EntityType.Italic:
            return f"_{text}_"
        elif self.type == EntityType.Underline:
            return f"__{text}__"
        elif self.type == EntityType.Strikethrough:
            return f"~~{text}~~"
        elif self.type == EntityType.Spoiler:
            return f"||{text}||"
        elif self.type == EntityType.Code:
            return f"`{text}`"
        elif self.type == EntityType.Codeblock:
            return f"```\n{text}\n```"
        elif self.type == EntityType.TextLink:
            return self._make_hyperlink(text, self.url)
        elif self.type == EntityType.Url:
            complete_url = self._complete_url(text)
            return self._make_hyperlink(text, complete_url)
        else:
            return text

    @property
    def one_way_markdown_offset(self):
        """
        One-way Markdown offset of the entity, i.e. how many characters are added to the left side of given text on
        Markdown conversion. Apart from TextLinks this is same as total added characters divided by two.
        Internally used especially in converting nested markdown in text.

        :return: Amount of characters added to both sides of string in Markdown for this entity.
        """
        if self.type == EntityType.TextLink:
            # TextLink has extra characters also in the middle, but only one character is added left side
            # e.g. www.example.com -> [www.example.com](www.example.com)
            return 1
        else:
            # For generic cases use simple calculation instead of hard coding
            tmp = "dummy"
            md = self.markdown(tmp)
            return (len(md) - len(tmp)) // 2


class MessageAutoDeleteTimerChanged:

    __slots__ = "message_auto_delete_time"

    def __init__(self, payload: MessageAutoDeleteTimerChangedPayload):
        self.message_auto_delete_time = payload["message_auto_delete_time"]


@flatten_handlers
class Message:

    __slots__ = (
        "message_id",
        "from_",
        "sender_chat",
        "date",
        "chat",
        "forward_from",
        "forward_from_chat",
        "forward_from_message_id",
        "forward_signature",
        "forward_sender_name",
        "forward_date",
        "is_automatic_forward",
        "reply_to_message",
        "via_bot",
        "edit_date",
        "has_protected_content",
        "media_group_id",
        "author_signature",
        "text",
        "entities",
        "animation",
        "audio",
        "document",
        "photo",
        "sticker",
        "video",
        "video_note",
        "voice",
        "caption",
        "caption_entities",
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
        "pinned_message"
    )

    def __init__(self, payload: MessagePayload) -> None:
        self._update(payload)

    # TODO: Figure out how to read variable 'from' to 'from_' from payload!
    def _update(self, payload: MessagePayload) -> None:
        self.message_id = payload["message_id"]
        self.date = payload["date"]
        self.chat = Chat(payload["chat"])
        self.from_ = payload.get("from_")
        self.sender_chat = payload.get("sender_chat")
        self.forward_from = payload.get("forward_from")
        self.forward_from_chat = payload.get("forward_from_chat")
        self.forward_from_message_id = payload.get("forward_from_message_id", -1)
        self.forward_signature = payload.get("forward_signature")
        self.forward_sender_name = payload.get("forward_sender_name")
        self.forward_date = payload.get("forward_date", -1)
        self.is_automatic_forward = payload.get("is_automatic_forward", False)
        self.reply_to_message = payload.get("reply_to_message")
        self.via_bot = payload.get("via_bot")
        self.edit_date = payload.get("edit_date", -1)
        self.has_protected_content = payload.get("has_protected_content", False)
        self.media_group_id = payload.get("media_group_id")
        self.author_signature = payload.get("author_signature")
        self.text = payload.get("text")
        self.entities: List[MessageEntity] = payload.get("entities", [])
        self.animation = payload.get("animation")
        self.audio = payload.get("audio")
        self.document = payload.get("document")
        self.photo = payload.get("photo", [])
        self.sticker = payload.get("sticker")
        self.video = payload.get("video")
        self.video_note = payload.get("video_note")
        self.voice = payload.get("voice")
        self.caption = payload.get("caption")
        self.caption_entities = payload.get("caption_entities", [])
        self.contact = payload.get("contact")
        self.dice = payload.get("dice")
        self.game = payload.get("game")
        self.poll = payload.get("poll")
        self.venue = payload.get("venue")
        self.location = payload.get("location")
        self.new_chat_members = payload.get("new_chat_members", [])
        self.left_chat_member = payload.get("left_chat_member")
        self.new_chat_title = payload.get("new_chat_title")
        self.new_chat_photo = payload.get("new_chat_photo", [])
        self.delete_chat_photo = payload.get("delete_chat_photo", False)
        self.group_chat_created = payload.get("group_chat_created", False)
        self.supergroup_chat_created = payload.get("supergroup_chat_created", False)
        self.channel_chat_created = payload.get("channel_chat_created", False)
        self.message_auto_delete_timer_changed = payload.get("message_auto_delete_timer_changed")
        self.migrate_to_chat_id = payload.get("migrate_to_chat_id", -1)
        self.pinned_message = payload.get("pinned_message")

        for key, func in self._HANDLERS:
            try:
                value = payload[key]  # type: ignore
            except KeyError:
                continue
            else:
                func(self, value)

    def _handle_from_(self, value):
        self.from_ = User(value)

    def _handle_sender_chat(self, value):
        self.sender_chat = Chat(value)

    def _handle_forward_from(self, value):
        self.forward_from = User(value)

    def _handle_forward_from_chat(self, value):
        self.forward_from_chat = Chat(value)

    def _handle_reply_to_message(self, value):
        self.reply_to_message = Message(value)

    def _handle_via_bot(self, value):
        self.via_bot = User(value)

    def _handle_entities(self, value):
        self.entities = [MessageEntity(e) for e in value]

    def _handle_animation(self, value):
        self.animation = Animation(value)

    def _handle_audio(self, value):
        self.audio = Audio(value)

    def _handle_document(self, value):
        self.document = Document(value)

    def _handle_photo(self, value):
        self.photo = [PhotoSize(p) for p in value]

    def _handle_sticker(self, value):
        self.sticker = Sticker(value)

    def _handle_video(self, value):
        self.video = Video(value)

    def _handle_video_note(self, value):
        self.video_note = VideoNote(value)

    def _handle_voice(self, value):
        self.voice = Voice(value)

    def _handle_caption_entities(self, value):
        self.caption_entities = [MessageEntity(e) for e in value]

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

    @property
    def text_formatted(self) -> str:
        """
        Telegram message content and entities combined into Markdown syntax
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

    def markdownify(self) -> str:
        """
        Apply message entities in Markdown syntax to the message content.

        :return: Message content with entities added in Markdown syntax.
        """
        markdownified = self.text
        grouped_entities = self._group_entities()
        total_offset = 0

        for offset_entities in grouped_entities.values():
            one_way_offset = total_offset  # Offset needed in nested entities
            for entity in offset_entities:
                offset = entity.offset + one_way_offset
                text_seq = markdownified[offset:offset+entity.length]
                entity_markdown = entity.markdown(text_seq)
                markdownified = markdownified[:offset] + entity_markdown + markdownified[offset+entity.length:]

                one_way_offset += entity.one_way_markdown_offset
                if entity.type == EntityType.TextLink or entity.type == EntityType.Url:
                    # TextLink has extra brackets, need to calculate the difference
                    total_offset += len(entity_markdown) - len(text_seq)
                else:
                    total_offset += entity.one_way_markdown_offset * 2

        return markdownified
