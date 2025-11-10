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


from typing_extensions import TypedDict, NotRequired

from .chat import Chat
from .user import User


# TODO: Combine/refactor the boost classes
class ChatBoostSource(TypedDict):
    source: str


class ChatBoostSourcePremium(ChatBoostSource):
    user: User


class ChatBoostSourceGiftCode(ChatBoostSource):
    user: User


class ChatBoostSourceGiveaway(ChatBoostSource):
    giveaway_message_id: int
    user: NotRequired[User]
    prize_star_count: NotRequired[int]
    is_unclaimed: NotRequired[bool]


class ChatBoost(TypedDict):
    boost_id: str
    add_date: int
    expiration_date: int
    source: ChatBoostSource


class ChatBoostRemoved(TypedDict):
    chat: Chat
    boost_id: str
    remove_date: int
    source: ChatBoostSource


class ChatBoostUpdated(TypedDict):
    chat: Chat
    boost: ChatBoost


class ChatBoostAdded(TypedDict):
    boost_count: int
