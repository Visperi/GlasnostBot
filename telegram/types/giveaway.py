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


from typing import List

from typing_extensions import TypedDict, NotRequired

from .chat import Chat
from .user import User


class GiveawayBase(TypedDict):
    winners_selection_date: int
    winner_count: int
    only_new_members: NotRequired[bool]
    prize_description: NotRequired[str]
    prize_star_count: NotRequired[int]
    premium_subscription_month_count: NotRequired[int]


class Giveaway(GiveawayBase):
    chats: List[Chat]
    has_public_winners: NotRequired[bool]
    country_codes: NotRequired[List[str]]


class GiveawayWinners(GiveawayBase):
    chat: Chat
    giveaway_message_id: int
    winners: List[User]
    additional_chat_count: NotRequired[int]
    unclaimed_prize_count: NotRequired[int]
    was_refunded: NotRequired[bool]


class GiveawayCreated(TypedDict):
    prize_star_count: NotRequired[int]
