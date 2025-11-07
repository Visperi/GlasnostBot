from .types.post import (
    SuggestedPostPrice as SuggestedPostPricePayload,
    SuggestedPostParameters as SuggestedPostParametersPayload,
    SuggestedPostInfo as SuggestedPostInfoPayload
)


class SuggestedPostPrice:

    __slots__ = (
        "currency",
        "amount"
    )

    def __init__(self, payload: SuggestedPostPricePayload):
        self.currency = payload["currency"]
        self.amount = payload["amount"]


class SuggestedPostParameters:

    __slots__ = (
        "price",
        "send_date"
    )

    def __init__(self, payload: SuggestedPostParametersPayload):
        self.send_date = payload.get("send_date", -1)

        try:
            self.price = SuggestedPostPrice(payload["price"])
        except KeyError:
            self.price = None


class SuggestedPostInfo(SuggestedPostParameters):

    __slots__ = (
        "state"
    )

    def __init__(self, payload: SuggestedPostInfoPayload):
        super().__init__(payload)
        self.state = payload["state"]
