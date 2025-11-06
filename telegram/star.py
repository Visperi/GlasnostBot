from .types.star import StarAmount as StarAmountPayload


class StarAmount:

    __slots__ = (
        "amount",
        "nanostar_amount"
    )

    def __init__(self, payload: StarAmountPayload):
        self.amount = payload["amount"]
        self.nanostar_amount = payload.get("nanostar_amount", 0)
