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


from .types.payments import (
    ShippingAddress as ShippingAddressPayload,
    OrderInfo as OrderInfoPayload,
    Invoice as InvoicePayload,
    Payment as PaymentPayload,
    SuccessfulPayment as SuccessfulPaymentPayload,
    RefundedPayment as RefundedPaymentPayload
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
        self.name = payload.get("name")
        self.phone_number = payload.get("phone_number")
        self.email = payload.get("email")

        try:
            self.shipping_address = ShippingAddress(payload["shipping_address"])
        except KeyError:
            self.shipping_address = None


class Invoice:

    __slots__ = (
        "title",
        "description",
        "start_parameter",
        "currency",
        "total_amount"
    )

    def __init__(self, payload: InvoicePayload):
        self.title = payload["title"]
        self.description = payload["description"]
        self.start_parameter = payload["start_parameter"]
        self.currency = payload["currency"]
        self.total_amount = payload["total_amount"]


class Payment:

    __slots__ = (
        "currency",
        "total_amount",
        "invoice_payload",
        "telegram_payment_charge_id"
    )

    def __init__(self, payload: PaymentPayload):
        self.currency = payload["currency"]
        self.total_amount = payload["total_amount"]
        self.invoice_payload = payload["invoice_payload"]
        self.telegram_payment_charge_id = payload["telegram_payment_charge_id"]


class SuccessfulPayment(Payment):

    __slots__ = (
        "provider_payment_charge_id",
        "subscription_expiration_date",
        "is_recurring",
        "is_first_recurring",
        "shipping_option_id",
        "order_info"
    )

    def __init__(self, payload: SuccessfulPaymentPayload):
        super().__init__(payload)
        self.provider_payment_charge_id = payload["provider_payment_charge_id"]
        self.subscription_expiration_date = payload.get("subscription_expiration_date")
        self.is_recurring = payload.get("is_recurring", False)
        self.is_first_recurring = payload.get("is_first_recurring", False)
        self.shipping_option_id = payload.get("shipping_option_id")

        try:
            self.order_info = OrderInfo(payload["order_info"])
        except KeyError:
            self.order_info = None


class RefundedPayment(Payment):

    __slots__ = (
        "provider_payment_charge_id"
    )

    def __init__(self, payload: RefundedPaymentPayload):
        super().__init__(payload)
        self.provider_payment_charge_id = payload.get("provider_payment_charge_id")
