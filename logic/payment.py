# third party imports
import stripe

# module imports
from exceptions import BaseError
from models.payment import PaymentBase


class PaymentLogic:
    def __init__(self, stripe_secret_key: str, stripe_product_map: dict[str, str], stripe_success_url: str, stripe_cancel_url: str):
        stripe.api_key = stripe_secret_key
        self._stripe_product_map = stripe_product_map
        self._stripe_success_url = stripe_success_url
        self._stripe_cancel_url = stripe_cancel_url

    async def create(self, products: PaymentBase, user_email: str):
        line_items = [{"price": self._stripe_product_map[product["id"]], "quantity": product["quantity"]} for product in products]
        try:
            return await stripe.checkout.Session.create(
                line_items=line_items,
                customer_email=user_email,
                mode="payment",
                stripe_success_url=self._stripe_success_url,
                stripe_cancel_url=self._stripe_cancel_url,
            )
        except Exception as e:
            raise BaseError({"code": "payment_base", "description": e}) from e
