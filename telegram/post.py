from .types.post import (
    SuggestedPostPrice as SuggestedPostPricePayload,
    SuggestedPostParameters as SuggestedPostParametersPayload,
    SuggestedPostInfo as SuggestedPostInfoPayload
)
from .types.message import (
    SuggestedPostEvent as SuggestedPostEventPayload,
    SuggestedPostApproved as SuggestedPostApprovedPayload,
    SuggestedPostApprovalFailed as SuggestedPostApprovalFailedPayload,
    SuggestedPostDeclined as SuggestedPostDeclinedPayload,
    SuggestedPostPaid as SuggestedPostPaidPayload,
    SuggestedPostRefunded as SuggestedPostRefundedPayload
)
from .star import StarAmount


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


class SuggestedPostEvent:

    __slots__ = (
        "suggested_post_message"
    )

    def __init__(self, payload: SuggestedPostEventPayload):
        try:
            self.suggested_post_message = payload.get("suggested_post_message")
        except KeyError:
            self.suggested_post_message = None


class SuggestedPostApproved(SuggestedPostEvent):

    __slots__ = (
        "price",
        "send_date"
    )

    def __init__(self, payload: SuggestedPostApprovedPayload):
        super().__init__(payload)
        self.send_date = payload["send_date"]

        try:
            self.price = SuggestedPostPrice(payload["price"])
        except KeyError:
            self.price = None


class SuggestedPostApprovalFailed(SuggestedPostEvent):

    __slots__ = (
        "price"
    )

    def __init__(self, payload: SuggestedPostApprovalFailedPayload):
        super().__init__(payload)
        self.price = SuggestedPostPrice(payload["price"])


class SuggestedPostDeclined(SuggestedPostEvent):

    __slots__ = (
        "comment"
    )

    def __init__(self, payload: SuggestedPostDeclinedPayload):
        super().__init__(payload)
        self.comment = payload.get("comment")


class SuggestedPostPaid(SuggestedPostEvent):

    __slots__ = (
        "currency",
        "amount",
        "star_amount"
    )

    def __init__(self, payload: SuggestedPostPaidPayload):
        super().__init__(payload)
        self.currency = payload["currency"]
        self.amount = payload.get("amount", -1)

        try:
            self.star_amount = StarAmount(payload["star_amount"])
        except KeyError:
            self.star_amount = None


class SuggestedPostRefunded(SuggestedPostEvent):

    __slots__ = (
        "reason"
    )

    def __init__(self, payload: SuggestedPostRefundedPayload):
        super().__init__(payload)
        self.reason = payload["reason"]
