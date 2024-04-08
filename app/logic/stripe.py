# third party imports
import stripe

# module imports
from app.exceptions import BaseError


class StripeLogic:
    def __init__(self, stripe_secret_key: str, stripe_product_map: dict[str, str], domain_url: str):
        stripe.api_key = stripe_secret_key
        self._stripe_product_map = stripe_product_map
        self._domain_url = domain_url

    async def create(self, products, user_email: str) -> str:
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[{"price": self._stripe_product_map[product["id"]], "quantity": product["quantity"]} for product in products],
                customer_email=user_email,
                mode="stripe",
                success_url=self._domain_url + "?success=true",
                cancel_url=self._domain_url + "?canceled=true",
                automatic_tax={"enabled": True},
            )
        except Exception as e:
            raise BaseError({"code": "stripe_base", "description": e}) from e
        return checkout_session.url
