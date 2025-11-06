from urllib.parse import urlparse, urlunparse
from typing import Optional

from .types.message_entity import MessageEntity as MessageEntityPayload
from .user import User


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
