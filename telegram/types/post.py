from typing_extensions import TypedDict, NotRequired


class SuggestedPostPrice(TypedDict):
    currency: str
    amount: int


class SuggestedPostParameters(TypedDict):
    price: NotRequired[SuggestedPostPrice]
    send_date: NotRequired[int]


class SuggestedPostInfo(SuggestedPostParameters):
    state: str
