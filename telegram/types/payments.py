"""
MIT License

Copyright (c) 2022 Niko Mätäsaho

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


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


class ShippingQuery(TypedDict):
    id: str
    from_: User
    invoice_payload: str
    shipping_address: ShippingAddress


class Invoice(TypedDict):
    title: str
    description: str
    start_parameter: str
    currency: str
    total_amount: int


class Payment(TypedDict):
    currency: str
    total_amount: int
    invoice_payload: str
    telegram_payment_charge_id: str


# TODO: How to differentiate successful payment and refunded payment?
class SuccessfulPayment(Payment):
    provider_payment_charge_id: str
    subscription_expiration_date: NotRequired[int]
    is_recurring: NotRequired[bool]
    is_first_recurring: NotRequired[bool]
    shipping_option_id: NotRequired[str]
    order_info: NotRequired[OrderInfo]

class RefundedPayment(Payment):
    provider_payment_charge_id: NotRequired[str]
