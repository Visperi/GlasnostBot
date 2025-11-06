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


from .types.poll import (
    PollOption as PollOptionPayload,
    PollAnswer as PollAnswerPayload,
    Poll as PollPayload,
    PollOptionBase as PollOptionBasePayload,
    InputPollOption as InputPollOptionPayload
)
from .message_entity import MessageEntity
from .user import User
from .chat import Chat


class PollOptionBase:

    __slots__ = (
        "text",
        "text_entities"
    )

    def __init__(self, payload: PollOptionBasePayload):
        self.text = payload["text"]

        try:
            self.text_entities = [MessageEntity(e) for e in payload["text_entities"]]
        except KeyError:
            self.text_entities = []


class PollOption(PollOptionBase):

    __slots__ = (
        "voter_count"
    )

    def __init__(self, payload: PollOptionPayload):
        super().__init__(payload)
        self.voter_count = payload["voter_count"]


class InputPollOption(PollOptionBase):

    __slots__ = (
        "text_parse_mode"
    )

    def __init__(self, payload: InputPollOptionPayload):
        super().__init__(payload)
        self.text_parse_mode = payload.get("text_parse_mode")


class PollAnswer:

    __slots__ = (
        "poll_id",
        "voter_chat",
        "user",
        "option_ids"
    )

    def __init__(self, payload: PollAnswerPayload):
        self.poll_id = payload["poll_id"]
        self.option_ids = payload["option_ids"]

        try:
            self.voter_chat = Chat(payload["voter_chat"])
        except KeyError:
            self.voter_chat = None

        try:
            self.user = User(payload["user"])
        except KeyError:
            self.user = None


class Poll:

    __slots__ = (
        "id",
        "question",
        "question_entities",
        "options",
        "total_voter_count",
        "is_closed",
        "is_anonymous",
        "type",
        "allows_multiple_answers",
        "correct_option_id",
        "explanation",
        "explanation_entities",
        "open_period",
        "close_date"
    )

    def __init__(self, payload: PollPayload):
        self.id = payload["id"]
        self.question = payload["question"]
        self.question_entities = payload.get("question_entities", [])
        self.options = [PollOption(o) for o in payload["options"]]
        self.total_voter_count = payload["total_voter_count"]
        self.is_closed = payload["is_closed"]
        self.is_anonymous = payload["is_anonymous"]
        self.type = payload["type"]
        self.allows_multiple_answers = payload["allows_multiple_answers"]
        self.correct_option_id = payload.get("correct_option_id", -1)
        self.explanation = payload.get("explanation")
        self.explanation_entities = payload.get("explanation_entities", [])
        self.open_period = payload.get("open_period", -1)
        self.close_date = payload.get("close_date", -1)

        self.question_entities = [MessageEntity(e) for e in self.question_entities]
        self.explanation_entities = [MessageEntity(e) for e in self.explanation_entities]
