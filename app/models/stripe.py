# standard lib imports
from typing import Any, Sequence

# third party imports
from pydantic import BaseModel, Field


class StripeBase(BaseModel):
    products: Sequence[dict[str, Any]] = Field(..., title="price_id:quantity array of order")
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "products": [
                        {"id": "Geneva", "quantity": 2},
                        {"id": "Juniper", "quantity": 4},
                    ]
                }
            ]
        }
    }
