from .types.poll import (
    PollOption as PollOptionPayload,
    PollAnswer as PollAnswerPayload,
    Poll as PollPayload
)


class PollOption:

    __slots__ = (
        "text",
        "voter_count"
    )

    def __init__(self, payload: PollOptionPayload):
        self.text = payload["text"]
        self.voter_count = payload["voter_count"]


class PollAnswer:

    __slots__ = (
        "poll_id",
        "user",
        "option_ids"
    )

    def __init__(self, payload: PollAnswerPayload):
        self.poll_id = payload["poll_id"]
        self.user = payload["user"]
        self.option_ids = payload["option_ids"]


class Poll:

    __slots__ = (
        "id",
        "question",
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
        self.__update(payload)

    def __update(self, payload: PollPayload):
        self.id = payload["id"]
        self.question = payload["question"]
        self.options = payload["options"]
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
