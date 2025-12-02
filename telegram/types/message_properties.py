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


from typing import TypedDict, NotRequired, List

from .user import User
from .chat import Chat
from .message_entity import MessageEntity


# TODO: Combine/refactor the message origin classes
class MessageOrigin(TypedDict):
    type: str
    date: int


class MessageOriginUser(MessageOrigin):
    sender_user: User


class MessageOriginHiddenUser(MessageOrigin):
    sender_user_name: str


class MessageOriginChat(MessageOrigin):
    sender_chat: Chat
    author_signature: NotRequired[str]


class MessageOriginChannel(MessageOrigin):
    chat: Chat
    message_id: int
    author_signature: NotRequired[str]


class DirectMessagesTopic(TypedDict):
    topic_id: int
    user: NotRequired[User]


class LinkPreviewOptions(TypedDict):
    is_disabled: NotRequired[bool]
    url: NotRequired[str]
    prefer_small_media: NotRequired[bool]
    prefer_large_media: NotRequired[bool]
    show_above_text: NotRequired[bool]


class TextQuote(TypedDict):
    text: str
    entities: NotRequired[List[MessageEntity]]
    position: int
    is_manual: NotRequired[bool]
