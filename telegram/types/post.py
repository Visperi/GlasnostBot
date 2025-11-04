from typing_extensions import TypedDict, NotRequired

from .message import Message
from .star import StarAmount


class SuggestedPostPrice(TypedDict):
    currency: str
    amount: int


class SuggestedPostParameters(TypedDict):
    price: NotRequired[SuggestedPostPrice]
    send_date: NotRequired[int]


class SuggestedPostInfo(TypedDict):
    state: str
    price: NotRequired[SuggestedPostPrice]
    send_date: NotRequired[int]


class SuggestedPostEvent(TypedDict):
    suggested_post_message: NotRequired[Message]


class SuggestedPostApproved(SuggestedPostEvent):
    price: NotRequired[SuggestedPostPrice]
    send_date: int


class SuggestedPostApprovalFailed(SuggestedPostEvent):
    price: SuggestedPostPrice


class SuggestedPostDeclined(SuggestedPostEvent):
    comment: NotRequired[str]


class SuggestedPostPaid(SuggestedPostEvent):
    currency: str
    amount: NotRequired[int]
    star_amount: NotRequired[StarAmount]


class SuggestedPostRefunded(SuggestedPostEvent):
    reason: str
