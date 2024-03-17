
# module imports
from exceptions import BaseError
from models.payment import PaymentBase
# third party imports
import stripe


class PaymentLogic:
    def __init__(self, stripe_secret_key: str, product_map: dict[str,str], success_url: str, cancel_url: str):
        stripe.api_key = stripe_secret_key
        self._product_map = product_map
        self._success_url = success_url
        self._cancel_url = cancel_url

    async def create(self, products: PaymentBase, user_email: str):
        line_items = [{"price": self._product_map[product["id"]], "quantity": self._product_map[product["quantity"]]} for product in products]
        try:
            return await stripe.checkout.Session.create(line_items=line_items, customer_email=user_email, mode="payment", 
                                                        success_url=self._success_url, cancel_url=self._cancel_url)
        except Exception as e:
            raise BaseError({"code": "payment_base", "description": e})