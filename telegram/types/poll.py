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
from .message_properties import MessageEntity


class PollOptionBase(TypedDict):
    text: str
    text_entities: NotRequired[List[MessageEntity]]


class InputPollOption(PollOptionBase):
    text_parse_mode: NotRequired[str]


class PollOption(PollOptionBase):
    voter_count: int


class PollAnswer(TypedDict):
    poll_id: str
    voter_chat: NotRequired[Chat]
    user: NotRequired[User]
    option_ids: List[int]


class Poll(TypedDict):
    id: str
    question: str
    question_entities: NotRequired[List[MessageEntity]]
    options: List[PollOption]
    total_voter_count: int
    is_closed: bool
    is_anonymous: bool
    type: str
    allows_multiple_answers: bool
    correct_option_id: NotRequired[int]
    explanation: NotRequired[str]
    explanation_entities: NotRequired[List[MessageEntity]]
    open_period: NotRequired[int]
    close_date: NotRequired[int]
