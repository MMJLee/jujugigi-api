# standard lib imports
from typing import Optional, Sequence

# third party imports
from databases import Database

# module imports
from app.models.user_image import UserImage, UserImageCreate, UserImageUpdate, UserRankings
from app.utils import build_insert_statement, build_update_statement


class UserImageData:
    def __init__(self, db: Database) -> None:
        self._db = db

    async def create(self, user_image: UserImageCreate) -> int:
        mapped_dict = user_image.model_dump()
        fields_statement, values_statement = build_insert_statement(mapped_dict=mapped_dict)
        return await self._db.fetch_val(
            query=f"""
                WITH create_user_image AS (
                    INSERT INTO user_image ({fields_statement})
                    VALUES ({values_statement}) RETURNING *
                ) SELECT COUNT(*) as created 
                FROM create_user_image;
            """,
            values=mapped_dict,
            column="created",
        )

    async def read(self, limit: int, offset: int) -> Sequence[Optional[UserImage]]:
        records = await self._db.fetch_all(query="SELECT * FROM user_image LIMIT :limit OFFSET :offset", values={"limit": limit, "offset": offset})
        return [UserImage(**dict(record)) for record in records]

    async def read_rankings(self, limit: int, offset: int) -> Sequence[Optional[UserRankings]]:
        records = await self._db.fetch_all(
            query="""
                SELECT * FROM rankings
                LIMIT :limit OFFSET :offset
            """,
            values={"limit": limit, "offset": offset},
        )
        return [UserRankings(**dict(record)) for record in records]

    async def update(self, user_image_id: int, user_image: UserImageUpdate) -> int:
        mapped_dict = user_image.model_dump()
        mapped_dict["user_image_id"] = user_image_id
        update_statement = build_update_statement(mapped_dict=mapped_dict)
        return await self._db.fetch_val(
            query=f"""
                WITH update_user_image as (
                    UPDATE user_image SET {update_statement}
                    WHERE user_image_id = :user_image_id RETURNING *
                ) SELECT COUNT(*) as updated 
                FROM update_user_image
            """,
            values=mapped_dict,
            column="updated",
        )

    async def delete(self, user_image_id: int) -> int:
        return await self._db.fetch_val(
            query="""
                WITH delete_user_image as (
                    DELETE FROM user_image 
                    WHERE user_image_id = :user_image_id RETURNING *
                ) SELECT count(*) as deleted 
                FROM delete_user_image;
            """,
            values={"user_image_id": user_image_id},
            column="deleted",
        )

    async def read_unopened_image(self, user_email: str) -> int:
        return await self._db.fetch_val(
            query="""
                WITH update_user_image as (
                    UPDATE user_image
                    SET opened = TRUE,
                    updated_on = CURRENT_TIMESTAMP
                    WHERE user_image_id = (
                        SELECT user_image_id
                        FROM user_image
                        WHERE user_email = :user_email 
                        AND opened = FALSE
                        ORDER BY created_on ASC LIMIT 1
                    ) RETURNING *
                ) SELECT user_image_id 
                FROM update_user_image
            """,
            values={"user_email": user_email},
            column="user_image_id",
        )
