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


from .user import User
from .types.payments import (
    ShippingAddress as ShippingAddressPayload,
    OrderInfo as OrderInfoPayload,
    PreCheckoutQuery as PreCheckoutQueryPayload
)


class ShippingAddress:

    __slots__ = (
        "country_code",
        "state",
        "city",
        "street_line1",
        "street_line2",
        "post_code"
    )

    def __init__(self, payload: ShippingAddressPayload):
        self.__update(payload)

    def __update(self, payload: ShippingAddressPayload):
        self.country_code = payload["country_code"]
        self.state = payload["state"]
        self.city = payload["city"]
        self.street_line1 = payload["street_line1"]
        self.street_line2 = payload["street_line2"]
        self.post_code = payload["post_code"]


class OrderInfo:

    __slots__ = (
        "name",
        "phone_number",
        "email",
        "shipping_address"
    )

    def __init__(self, payload: OrderInfoPayload):
        self.__update(payload)

    def __update(self, payload: OrderInfoPayload):
        self.name = payload.get("name")
        self.phone_number = payload.get("phone_number")
        self.email = payload.get("email")

        try:
            self.shipping_address = ShippingAddress(payload["shipping_address"])
        except KeyError:
            self.shipping_address = None


class PreCheckoutQuery:

    __slots__ = (
        "id",
        "from_",
        "currency",
        "total_amount",
        "invoice_payload",
        "shipping_option_id",
        "order_info"
    )

    def __init__(self, payload: PreCheckoutQueryPayload):
        self.__update(payload)

    # TODO: Figure out how to read variable 'from' to 'from_' from payload!
    def __update(self, payload: PreCheckoutQueryPayload):
        self.id = payload["id"]
        self.from_ = User(payload["from_"])
        self.currency = payload["currency"]
        self.total_amount = payload["total_amount"]
        self.invoice_payload = payload["invoice_payload"]
        self.shipping_option_id = payload.get("shipping_option_id")

        try:
            self.order_info = OrderInfo(payload["order_info"])
        except KeyError:
            self.order_info = None
