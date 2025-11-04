from typing_extensions import TypedDict, NotRequired

from .message import Message
from .star import StarAmount


class SuggestedPostPrice(TypedDict):
    currency: str
    amount: int


class SuggestedPostInfo(TypedDict):
    state: str
    price: NotRequired[SuggestedPostPrice]
    send_date: NotRequired[int]


class SuggestedPostApproved(TypedDict):
    suggested_post_message: NotRequired[Message]
    price: NotRequired[SuggestedPostPrice]
    send_date: int


class SuggestedPostApprovalFailed(TypedDict):
    suggested_post_message: NotRequired[Message]
    price: SuggestedPostPrice


class SuggestedPostDeclined(TypedDict):
    suggested_post_message: NotRequired[Message]
    comment: NotRequired[str]


class SuggestedPostPaid(TypedDict):
    suggested_post_message: NotRequired[Message]
    currency: str
    amount: NotRequired[int]
    star_amount: NotRequired[StarAmount]


class SuggestedPostRefunded(TypedDict):
    suggested_post_message: NotRequired[Message]
    reason: str
