from typing import List
from typing_extensions import TypedDict, NotRequired
from .user import User
from .message import MessageEntity


class PollOption(TypedDict):
    text: str
    voter_count: int


class PollAnswer(TypedDict):
    poll_id: str
    user: User
    option_ids: List[int]


class Poll(TypedDict):
    id: str
    question: str
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
