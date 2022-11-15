from typing_extensions import TypedDict, NotRequired
from .user import User


class ShippingAddress(TypedDict):
    country_code: str
    state: str
    city: str
    street_line1: str
    street_line2: str
    post_code: str


class OrderInfo(TypedDict):
    name: NotRequired[str]
    phone_number: NotRequired[str]
    email: NotRequired[str]
    shipping_address: NotRequired[ShippingAddress]


class PreCheckoutQuery(TypedDict):
    id: str
    from_: User
    currency: str
    total_amount: int
    invoice_payload: str
    shipping_option_id: NotRequired[str]
    order_info: NotRequired[OrderInfo]
