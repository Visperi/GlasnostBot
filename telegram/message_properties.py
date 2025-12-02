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


from typing import Union, List

from .user import User
from .chat import Chat
from .message_entity import MessageEntity
from .types.message_properties import (
    MessageOrigin as MessageOriginPayload,
    MessageOriginUser as MessageOriginUserPayload,
    MessageOriginHiddenUser as MessageOriginHiddenUserPayload,
    MessageOriginChat as MessageOriginChatPayload,
    MessageOriginChannel as MessageOriginChannelPayload,
    DirectMessagesTopic as DirectMessagesTopicPayload,
    LinkPreviewOptions as LinkPreviewOptionsPayload,
    TextQuote as TextQuotePayload
)


class MessageOrigin:

    __slots__ = (
        "type",
        "date"
    )

    def __init__(self, payload: MessageOriginPayload):
        self.type = payload["type"]
        self.date = payload["date"]

    @property
    def sender(self) -> Union[User, str, Chat]:
        """
        :return: Original sender for the message. The origin type is ``telegram.User`` for messages originally sent by a
                 known users, or ``Chat`` for messages in channel chats and messages sent behalf of chat into groups.
                 For unknown users the origin is their Telegram username as a string.
        :raises ValueError: If the origin type is unknown and correct origin attribute cannot be fetched.
        """
        if isinstance(self, MessageOriginUser):
            return self.sender_user
        elif isinstance(self, MessageOriginHiddenUser):
            return self.sender_user_name
        elif isinstance(self, MessageOriginChat):
            return self.sender_chat
        elif isinstance(self, MessageOriginChannel):
            return self.chat
        else:
            raise ValueError(f"Unknown MessageOrigin instance type: {type(self)}")


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
