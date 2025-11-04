from typing_extensions import TypedDict, NotRequired


class StarAmount(TypedDict):
    amount: int
    nanostar_amount: NotRequired[int]
