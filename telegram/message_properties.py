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


from urllib.parse import urlparse, urlunparse
from typing import Tuple, Union, List
from enum import Enum

from .user import User
from .chat import Chat
from .types.message_properties import (
    MessageOrigin as MessageOriginPayload,
    MessageOriginUser as MessageOriginUserPayload,
    MessageOriginHiddenUser as MessageOriginHiddenUserPayload,
    MessageOriginChat as MessageOriginChatPayload,
    MessageOriginChannel as MessageOriginChannelPayload,
    DirectMessagesTopic as DirectMessagesTopicPayload,
    LinkPreviewOptions as LinkPreviewOptionsPayload,
    MessageEntity as MessageEntityPayload,
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


class EntityType(Enum):
    """
    Enum class that represents a type of message entity.
    """

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
    BlockQuote = "blockquote"
    ExpandableBlockQuote = "expandable_blockquote"

    @property
    def supports_markdown(self) -> bool:
        """
        :return: True if the entity type supports Markdown formatting, False otherwise.
        """
        return self not in [
            self.Mention,
            self.Hashtag,
            self.Cashtag,
            self.BotCommand,
            self.Email,
            self.PhoneNumber,
            self.TextMention,
            self.CustomEmoji,
            self.ExpandableBlockQuote
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
        """
        Represents a message entity in a Telegram message.

        :param payload: MessageEntity payload as a dictionary from Telegram API.
        """
        self.type = EntityType(payload["type"])
        """
        Type of the message entity.
        """
        self.offset = payload["offset"]
        """
        Offset in UTF-16 code units to the start of the entity.
        """
        self.length = payload["length"]
        """
        Length of the entity in UTF-16 code units.
        """
        self.url = payload.get("url")
        """
        URL of a link in an entity of type ``EntityType.TextLink``.
        """
        self.language = payload.get("language")
        """
        Programming language for an entity of type ``EntityType.Codeblock``.
        """
        self.custom_emoji_id = payload.get("custom_emoji_id")
        """
        An ID for a custom emoji for entity type of ``EntityType.CustomEmoji``.
        """

        try:
            self.user = User(payload["user"])
            """
            A mentioned user for entity type of ``EntityType.TextMention``.
            """
        except KeyError:
            self.user = None

    @staticmethod
    def _complete_url(url: str) -> str:
        """
        Complete partial url so that it has scheme and starts with www. Does nothing for already complete urls.

        :param url: Url to be completed.
        :return: Completed url including scheme and starting with www.
        """
        tmp = urlparse(url, "http")
        netloc = tmp.netloc or tmp.path
        path = tmp.path if tmp.netloc else ""

        filled = tmp._replace(netloc=netloc, path=path)
        return str(urlunparse(filled))

    def markdown(self, text: str, make_url_to_hyperlink: bool) -> Tuple[str, int]:
        """
        Convert entity to Markdown syntax with given text.

        :param text: Content for the Markdown conversion.
        :param make_url_to_hyperlink: Make ``EntityType.Url`` entities to hyperlinks. The original text will not be
                                      modified. The original text is returned if the URL is already complete and a
                                      hyperlink cannot be made.
        :return: Given text converted to Entity Markdown syntax and the length increase compared to the original text.
        """
        if not self.type.supports_markdown:
            return text, 0

        # TODO: Should these somehow be properties instead?
        markdowns = {
            EntityType.Bold: {
                "before": "**",
                "after": "**"
            },
            EntityType.Italic: {
                "before": "*",
                "after": "*"
            },
            EntityType.Underline: {
                "before": "__",
                "after": "__"
            },
            EntityType.Strikethrough: {
                "before": "~~",
                "after": "~~"
            },
            EntityType.Spoiler: {
                "before": "||",
                "after": "||"
            },
            EntityType.Code: {
                "before": "`",
                "after": "`"
            },
            EntityType.Codeblock: {
                "before": "```{}\n",
                "after": "\n```"
            },
            EntityType.TextLink: {
                "before": "[",
                "after": "]({})"
            },
            EntityType.Url: {
                "before": "",
                "after": ""
            },
            EntityType.BlockQuote: {
                "before": "> ",
                "after": ""
            }
        }

        if self.type == EntityType.Url and make_url_to_hyperlink:
            markdown_syntax = markdowns[EntityType.TextLink]
        else:
            markdown_syntax = markdowns[self.type]

        before_text = markdown_syntax["before"]
        after_text = markdown_syntax["after"]
        if self.type == EntityType.Codeblock:
            before_text = before_text.format(self.language or "")
        if self.type == EntityType.TextLink:
            after_text = after_text.format(self.url)
        elif self.type == EntityType.Url and make_url_to_hyperlink:
            url = self._complete_url(text)
            if text == url:
                return text, 0
            after_text = after_text.format(url)

        return f"{before_text}{text}{after_text}", len(before_text) + len(after_text)

    def nested_markdown(self, text: str, message_entities: List['MessageEntity'], make_urls_to_hyperlinks: bool):
        """
        Apply nested markdown to the message entity.

        :param text: Text to add the markdown for.
        :param message_entities: List of ``MessageEntity`` objects to combine with this message entity.
        :param make_urls_to_hyperlinks: Make bare text urls to hyperlinks.
        :return: The text with all given message entity markdowns applied and the length increase compared to
                 the original text.
        """
        output, cumulative_offset = self.markdown(text, make_urls_to_hyperlinks)
        for entity in message_entities:
            output, added_offset = entity.markdown(output, make_urls_to_hyperlinks)
            cumulative_offset += added_offset

        return output, cumulative_offset


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
