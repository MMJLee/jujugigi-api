# standard lib imports
from typing import Sequence, Optional
from datetime import datetime
from zoneinfo import ZoneInfo
# module imports
from exceptions import BaseError
from data.image import ImageData
from models.image import Image, ImageBase, ImageCreate, ImageResponse, ImageUpdate
# third party imports
import stripe


class PaymentLogic:
    def __init__(self, stripe_secret_key: str):
        stripe.api_key = stripe_secret_key
        
    async def process_payment(self, amount: int):
        try:
            charge = stripe.PaymentIntent.create(amount=amount, currency="usd", automatic_payment_methods={"enabled": True})
            return charge.id
        except stripe.CardError as e:
            raise BaseError({"code": "payment", "description": e})
        except stripe.StripeError as e:
            raise BaseError({"code": "payment", "description": "Something went wrong. Please try again later."})