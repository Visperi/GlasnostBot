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


from enum import Enum
from urllib.parse import urlparse, urlunparse
from typing import Tuple, List

from .user import User
from .types.message_entity import MessageEntity as MessageEntityPayload


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
        True if the entity type supports Markdown formatting, False otherwise.
        """
        return self not in [
            self.Mention,
            self.Hashtag,
            self.Cashtag,
            self.BotCommand,
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

    @staticmethod
    def text_is_url(text) -> bool:
        """
        Check if a text is a complete URL.

        :param text: The text.
        :return: True if the text is URL, False otherwise.
        """
        try:
            result = urlparse(text)
            return all([result.scheme, result.netloc])
        except KeyError:
            return False

    def markdown(self, text: str, make_url_to_hyperlink: bool, allow_hyperlink_text_schema: bool = False) -> Tuple[str, int]:
        """
        Convert entity to Markdown syntax with given text.

        :param text: Content for the Markdown conversion.
        :param make_url_to_hyperlink: Make ``EntityType.Url`` entities to hyperlinks. The original text will not be
                                      modified. The original text is returned if the URL is already complete and a
                                      hyperlink cannot be made.
        :param allow_hyperlink_text_schema: Allow hyperlink text to contain the URL schema. Some Markdown processors
                                            do not render hyperlinks properly when there is a URL schema in the
                                            hyperlink text. If False, such link is formatted as plain URL instead.
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
            },
            EntityType.Email: {
                "before": "<",
                "after": ">"
            },
            EntityType.PhoneNumber: {
                "before": "<",
                "after": ">"
            }
        }

        markdown_syntax = markdowns[self.type]
        before_text = markdown_syntax["before"]
        after_text = markdown_syntax["after"]
        if self.type == EntityType.Codeblock:
            before_text = before_text.format(self.language or "")
        elif self.type == EntityType.TextLink:
            if not allow_hyperlink_text_schema and self.text_is_url(text):
                markdown_syntax = markdowns[EntityType.Url]
                before_text = markdown_syntax["before"]
                after_text = markdown_syntax["after"]
            else:
                after_text = after_text.format(self.url)
        elif self.type == EntityType.Url and make_url_to_hyperlink:
            url = self._complete_url(text)
            if text != url:
                markdown_syntax = markdowns[EntityType.TextLink]
                before_text = markdown_syntax["before"]
                after_text = markdown_syntax["after"].format(url)

        return f"{before_text}{text}{after_text}", len(before_text) + len(after_text)

    def nested_markdown(self,
                        text: str, message_entities: List['MessageEntity'],
                        make_urls_to_hyperlinks: bool,
                        allow_hyperlink_text_schema: bool = False):
        """
        Apply nested markdown to the message entity.

        :param text: Text to add the markdown for.
        :param message_entities: List of ``MessageEntity`` objects to combine with this message entity.
        :param make_urls_to_hyperlinks: Make bare text urls to hyperlinks.
        :param allow_hyperlink_text_schema: Allow hyperlink text to contain the URL schema. Some Markdown processors
                                            do not render hyperlinks properly when there is a URL schema in the
                                            hyperlink text. If False, such link is formatted as plain URL instead.
        :return: The text with all given message entity markdowns applied and the length increase compared to
                 the original text.
        """
        output, cumulative_offset = self.markdown(text, make_urls_to_hyperlinks)
        for entity in message_entities:
            output, added_offset = entity.markdown(output, make_urls_to_hyperlinks, allow_hyperlink_text_schema)
            cumulative_offset += added_offset

        return output, cumulative_offset
