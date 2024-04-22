# standard lib imports
from typing import Any
from datetime import datetime

# third party imports
from pydantic import BaseModel, Field, HttpUrl


class StripeWebhook(BaseModel):
    event_id: str = Field(..., title="stripe event id", alias="id")
    object: str = Field(..., title="stripe object")
    api_version: datetime = Field(..., title="datetime of stripe api version")
    created_on: datetime = Field(..., title="creation time of stripe object", alias="created")
    data: dict[str, dict[str, Any]] = Field(..., title="data of stripe object")
    livemode: bool = Field(..., title="live mode of stripe object")
    pending_webhooks: int = Field(..., title="pending webhook count of stripe object")
    request: dict[str, Any] = Field(..., title="request detail of stripe object")
    type: str = Field(..., title="type of stripe object")
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "event_id": "evt_3P5KxbAHPBlca9bB3kC8OYW4",
                    "object": "event",
                    "api_version": "2023-10-16",
                    "created": 1713069997,
                    "data": {
                        "object": {
                            "id": "pi_3P5KxbAHPBlca9bB3fQCtXMF",
                            "object": "payment_intent",
                            "amount": 99,
                            "amount_capturable": 0,
                            "amount_details": {"tip": {}},
                            "amount_received": 99,
                            "application": None,
                            "application_fee_amount": None,
                            "automatic_payment_methods": None,
                            "canceled_at": None,
                            "cancellation_reason": None,
                            "capture_method": "automatic",
                            "client_secret": "pi_3P5KxbAHPBlca9bB3fQCtXMF_secret_H3yqnOYR0XLliLzzm6JA7wcND",
                            "confirmation_method": "automatic",
                            "created": 1713069995,
                            "currency": "usd",
                            "customer": None,
                            "description": None,
                            "invoice": None,
                            "last_payment_error": None,
                            "latest_charge": "ch_3P5KxbAHPBlca9bB3dzhrIxo",
                            "livemode": False,
                            "metadata": {},
                            "next_action": None,
                            "on_behalf_of": None,
                            "payment_method": "pm_1P5KxbAHPBlca9bBztI0ik7R",
                            "payment_method_configuration_details": None,
                            "payment_method_options": {
                                "card": {"installments": None, "mandate_options": None, "network": None, "request_three_d_secure": "automatic"}
                            },
                            "payment_method_types": ["card"],
                            "processing": None,
                            "receipt_email": None,
                            "review": None,
                            "setup_future_usage": None,
                            "shipping": None,
                            "source": None,
                            "statement_descriptor": None,
                            "statement_descriptor_suffix": None,
                            "status": "succeeded",
                            "transfer_data": None,
                            "transfer_group": None,
                        }
                    },
                    "livemode": False,
                    "pending_webhooks": 2,
                    "request": {"id": "req_6NOdJXhQfm7odl", "idempotency_key": "a69248ee-efe1-4ef2-a33d-1d0d78deca9b"},
                    "type": "payment_intent.succeeded",
                }
            ]
        }
    }


class StripeResponse(BaseModel):
    url: HttpUrl = Field(..., title="redirect url for stripe checkout")
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "url": "https://example.com",
                }
            ],
        }
    }
