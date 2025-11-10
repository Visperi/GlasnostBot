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
from typing import Optional

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
        self.type = payload["type"]
        self.offset = payload["offset"]
        self.length = payload["length"]
        self.url = payload.get("url")
        self.language = payload.get("language")
        self.custom_emoji_id = payload.get("custom_emoji_id")

        try:
            self.user = User(payload["user"])
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

    @staticmethod
    def _make_hyperlink(text: str, url: str) -> str:
        """
        Convert bare text to a hyperlink.

        :param text: Hyperlink text
        :param url: Hyperlink url
        :return: Hyperlink with given text and url
        """
        return f"[{text}]({url})"

    def markdown(self, text: str, make_url_to_hyperlink: bool) -> Optional[str]:
        """
        Convert entity to Markdown syntax with given text.

        :param text: Content for the Markdown conversion.
        :param make_url_to_hyperlink: Make bare text urls to hyperlinks.
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
            if make_url_to_hyperlink:
                return self._make_hyperlink(text, complete_url)
            else:
                return complete_url
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
            tmp = "__dummy__"
            md = self.markdown(tmp, False)
            return (len(md) - len(tmp)) // 2


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
