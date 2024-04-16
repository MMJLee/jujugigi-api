# standard lib imports
import json
from typing import Optional, Sequence

# third party imports
from databases import Database

# module imports
from app.models.stripe import StripeWebhook
from app.utils import build_insert_statement, build_update_statement


class StripeData:
    def __init__(self, db: Database) -> None:
        self._db = db

    async def read(self, limit: int, offset: int) -> Sequence[Optional[StripeWebhook]]:
        records = await self._db.fetch_all(query="SELECT * FROM stripe LIMIT :limit OFFSET :offset", values={"limit": limit, "offset": offset})
        return [StripeWebhook(**dict(record)) for record in records]

    async def upsert(self, stripe_update: StripeWebhook) -> int:
        mapped_dict = stripe_update.model_dump()
        mapped_dict["data"] = json.dumps(mapped_dict["data"])
        mapped_dict["request"] = json.dumps(mapped_dict["request"])
        fields_statement, values_statement = build_insert_statement(mapped_dict=mapped_dict)
        update_statement = build_update_statement(mapped_dict=mapped_dict)
        return await self._db.fetch_val(
            query=f"""
            WITH upsert_stripe as (
                INSERT INTO stripe ({fields_statement})
                    VALUES ({values_statement})
                    ON CONFLICT (event_id)
                DO UPDATE SET {update_statement}
                    RETURNING *
                ) SELECT COUNT(*) as updated 
                FROM upsert_stripe
            """,
            values=mapped_dict,
            column="updated",
        )
