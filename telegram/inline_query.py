from .types.inline_query import (
    InlineQueryBase as InlineQueryBasePayload,
    InlineQuery as InlineQueryPayload,
    CallbackQuery as CallbackQueryPayload,
    ShippingQuery as ShippingQueryPayload,
    PreCheckoutQuery as PreCheckoutQueryPayload,
    ChosenInlineResult as ChosenInlineResultPayload
)


class InlineQueryBase:

    __slots__ = (
        "id",
        "from_"
    )

    def __init__(self, payload: InlineQueryBasePayload):
        self.id = payload["id"]
        self.from_ = payload["from_"]


class InlineQuery(InlineQueryBase):

    __slots__ = (
        "query",
        "offset",
        "chat_type",
        "location"
    )

    def __init__(self, payload: InlineQueryPayload):
        super().__init__(payload)
        self.__update(payload)

    def __update(self, payload: InlineQueryPayload):
        self.query = payload["query"]
        self.offset = payload["offset"]
        self.chat_type = payload.get("chat_type")
        self.location = payload.get("location")


class CallbackQuery(InlineQueryBase):

    __slots__ = (
        "message",
        "inline_message_id",
        "chat_instance",
        "data",
        "game_short_name"
    )

    def __init__(self, payload: CallbackQueryPayload):
        super().__init__(payload)
        self.__update(payload)

    def __update(self, payload: CallbackQueryPayload):
        self.message = payload.get("message")
        self.inline_message_id = payload.get("inline_message_id")
        self.chat_instance = payload["chat_instance"]
        self.data = payload.get("data")
        self.game_short_name = payload.get("game_short_name")


class ShippingQuery(InlineQueryBase):

    __slots__ = (
        "invoice_payload",
        "shipping_address"
    )

    def __init__(self, payload: ShippingQueryPayload):
        super().__init__(payload)
        self.__update(payload)

    def __update(self, payload: ShippingQueryPayload):
        self.invoice_payload = payload["invoice_payload"]
        self.shipping_address = payload["shipping_address"]


class PreCheckoutQuery(InlineQueryBase):

    __slots__ = (
        "currency",
        "total_amount",
        "invoice_payload",
        "shipping_option_id",
        "order_info"
    )

    def __init__(self, payload: PreCheckoutQueryPayload):
        super().__init__(payload)
        self.__update(payload)

    def __update(self, payload: PreCheckoutQueryPayload):
        self.currency = payload["currency"]
        self.total_amount = payload["total_amount"]
        self.invoice_payload = payload["invoice_payload"]
        self.shipping_option_id = payload.get("shipping_option_id")
        self.order_info = payload.get("order_info")


class ChosenInlineResult:

    __slots__ = (
        "result_id",
        "from_",
        "location",
        "inline_message_id",
        "query"
    )

    def __init__(self, payload: ChosenInlineResultPayload):
        self.__update(payload)

    def __update(self, payload: ChosenInlineResultPayload):
        self.result_id = payload["result_id"]
        self.from_ = payload["from_"]
        self.location = payload.get("location")
        self.inline_message_id = payload.get("inline_message_id")
        self.query = payload.get("query")
