# standard lib imports
import json

# third party imports
import stripe

# module imports
from app.data.stripe import StripeData
from app.exceptions import BaseError
from app.logic.image import ImageLogic
from app.models.stripe import StripeWebhook


class StripeLogic:
    def __init__(
        self,
        stripe_data: StripeData,
        stripe_secret_key: str,
        stripe_price_id: str,
        stripe_webhook_secret: str,
        domain_url: str,
        image_logic: ImageLogic,
    ):
        stripe.api_key = stripe_secret_key
        self._stripe_data = stripe_data
        self._stripe_price_id = stripe_price_id
        self._stripe_webhook_secret = stripe_webhook_secret
        self._domain_url = domain_url
        self._image_logic = image_logic

    async def create(self, user_email: str) -> str:
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[{"price": self._stripe_price_id, "quantity": 1}],
                customer_email=user_email,
                mode="payment",
                success_url=self._domain_url + "/success",
                cancel_url=self._domain_url,
                automatic_tax={"enabled": True},
            )
        except Exception as e:
            raise BaseError({"code": "stripe_create", "description": e}) from e

        return checkout_session.url

    async def webhook(self, stripe_response_header: str, stripe_response_body: bytes) -> int:

        try:
            _ = stripe.Webhook.construct_event(payload=stripe_response_body, sig_header=stripe_response_header, secret=self._stripe_webhook_secret)
            stripe_response_body_json = json.loads(stripe_response_body.decode("utf-8"))
            payment_id = "error"
            event_type = stripe_response_body_json["type"]
            if event_type == "charge.succeeded":
                payment_id = stripe_response_body_json["data"]["object"]["payment_intent"]
                await self._image_logic.gacha(stripe_response_body_json["data"]["object"]["billing_details"]["email"])
            elif event_type == "payment_intent.succeeded":
                payment_id = stripe_response_body_json["data"]["object"]["id"]

            stripe_response_body_obj = StripeWebhook(payment_id=payment_id, **stripe_response_body_json)
            return await self._stripe_data.upsert(stripe_update=stripe_response_body_obj)
        except KeyError as e:
            raise BaseError({"code": "stripe_email", "description": e}) from e
        except ValueError as e:
            raise BaseError({"code": "stripe_value", "description": e}) from e
        except stripe.error.SignatureVerificationError as e:
            raise BaseError({"code": "stripe_webhook", "description": e}) from e
