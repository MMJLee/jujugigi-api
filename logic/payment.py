
# module imports
from exceptions import BaseError
# third party imports
import stripe


class PaymentLogic:
    def __init__(self, stripe_secret_key: str):
        stripe.api_key = stripe_secret_key
        
    async def process_payment(self, amount: int):
        try:
            charge = stripe.PaymentIntent.create(amount=amount, currency="usd", confirm=True, automatic_payment_methods={"enabled": True})
            return charge.id
        except stripe.CardError as e:
            raise BaseError({"code": "payment", "description": e})
        except stripe.StripeError as e:
            raise BaseError({"code": "payment", "description": "Something went wrong. Please try again later."})
        except Exception as e:
            raise BaseError({"code": "payment_base", "description": e})