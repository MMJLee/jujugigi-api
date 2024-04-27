# standard lib imports
import json

# third party imports
import stripe

# module imports
from app.data.image import ImageData
from app.data.stripe import StripeData
from app.data.user_image import UserImageData
from app.exceptions import BaseError
from app.models.stripe import StripeWebhook
from app.models.user_image import UserImageCreate


class StripeLogic:
    def __init__(
        self,
        stripe_data: StripeData,
        stripe_secret_key: str,
        stripe_price_id: str,
        stripe_webhook_secret: str,
        domain_url: str,
        image_data: ImageData,
        user_image_data: UserImageData,
    ):
        stripe.api_key = stripe_secret_key
        self._stripe_data = stripe_data
        self._stripe_price_id = stripe_price_id
        self._stripe_webhook_secret = stripe_webhook_secret
        self._domain_url = domain_url
        self._image_data = image_data
        self._user_image_data = user_image_data

    async def read(self, user_email: str, quantity: int) -> str:
        records = await self._image_data.read_random_unowned_images(user_email=user_email, quantity=quantity)
        if len(records) != quantity:
            raise BaseError({"code": "gacha", "description": "You already own all images"})
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[{"price": self._stripe_price_id, "quantity": quantity}],
                customer_email=user_email,
                mode="payment",
                allow_promotion_codes=True,
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
            event_type = stripe_response_body_json["type"]
            if event_type == "checkout.session.completed":
                await self.gacha(user_email=stripe_response_body_json["data"]["object"]["customer_details"]["email"], quantity=2)
            stripe_response_body_obj = StripeWebhook(**stripe_response_body_json)
            return await self._stripe_data.upsert(stripe_update=stripe_response_body_obj)
        except KeyError as e:
            raise BaseError({"code": "stripe_email", "description": e}) from e
        except ValueError as e:
            raise BaseError({"code": "stripe_value", "description": e}) from e
        except stripe.error.SignatureVerificationError as e:
            raise BaseError({"code": "stripe_webhook", "description": e}) from e

    async def gacha(self, user_email: str, quantity: int) -> int:
        count = 0
        image_ids = await self._image_data.read_random_unowned_images(user_email=user_email, quantity=quantity)
        for image_id in image_ids:
            count += await self._user_image_data.create(
                user_image=UserImageCreate(user_email=user_email, image_id=image_id, opened=False, created_by=user_email, updated_by=user_email)
            )
        return count
