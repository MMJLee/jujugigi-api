# standard lib imports
from typing import Optional, Sequence

# third party imports
from databases import Database
from fastapi import UploadFile
from supabase import Client, StorageException
from asyncpg.exceptions import UniqueViolationError

# module imports
from exceptions import BaseError
from models.image import ImageCreate, ImageResponse, ImageUpdate
from utils import build_insert_statement, build_update_statement, log


class ImageData:
    def __init__(self, db: Database, supabase_client: Client, supabase_bucket: str, supabase_url_timeout: int) -> None:
        self._db = db
        self._supabase_client = supabase_client
        self._supabase_bucket = supabase_bucket
        self._supabase_url_timeout = supabase_url_timeout

    async def create(self, image: ImageCreate, image_file: UploadFile) -> int:
        try:
            self._supabase_client.storage.from_(self._supabase_bucket).upload(
                path=f"images/{image_file.filename}", file=image_file.file.read(), file_options={"content-type": image_file.content_type}
            )
        except StorageException:  # if dupe, continue to adding database record
            pass
        except Exception as e:
            raise BaseError({"code": "create:image", "description": e}) from e

        mapped_dict = image.model_dump()
        fields_statement, values_statement = build_insert_statement(image.model_dump())

        try:
            return await self._db.fetch_val(
                query=f"""
                    WITH create_image AS (
                        INSERT INTO image({fields_statement})
                        VALUES({values_statement}) RETURNING *
                    ) SELECT COUNT(*) as created 
                    FROM create_image;
                """,
                values=mapped_dict,
                column="created",
            )
        except UniqueViolationError:  # if dupe, return created
            return 1
        except Exception as e:
            raise BaseError({"code": "create:image", "description": e}) from e

    async def read(
        self, image_id: Optional[int] = None, name: Optional[str] = None, user_email: Optional[str] = None, limit: int = 50, offset: int = 0
    ) -> Sequence[Optional[ImageResponse]]:
        filter_statement = ""
        values = {"limit": limit, "offset": offset}

        if image_id:
            filter_statement = "WHERE i.image_id = :image_id"
            values["image_id"] = image_id
        elif name:
            filter_statement = "WHERE i.name = :name"
            values["name"] = name
        elif user_email:
            filter_statement = "JOIN user_image ui ON i.image_id = ui.image_id WHERE ui.user_email = :user_email"
            values["user_email"] = user_email

        records = await self._db.fetch_all(
            query=f"""
                SELECT i.* FROM image i
                {filter_statement}
                LIMIT :limit OFFSET :offset
            """,
            values=values,
        )
        if records:
            paths = [f"{record.path}/{record.name}" for record in records]
            image_details = self._supabase_client.storage.from_(self._supabase_bucket).create_signed_urls(paths=paths, expires_in=self._supabase_url_timeout)
            image_response = []
            for i, record in enumerate(records):
                image_response.append(ImageResponse(**dict(record), signedURL=image_details[i].get("signedURL")))
        return image_response

    async def update(self, image_id: int, image: ImageUpdate) -> int:
        mapped_dict = image.model_dump()
        mapped_dict["image_id"] = image_id
        update_statement = build_update_statement(mapped_dict=mapped_dict)

        return await self._db.fetch_val(
            query=f"""
                WITH update_image as (
                    UPDATE image SET {update_statement}
                    WHERE image_id = :image_id RETURNING *
                ) SELECT COUNT(*) as updated 
                FROM update_image
            """,
            values=mapped_dict,
            column="updated",
        )

    async def delete(self, image_id: int) -> int:
        return await self._db.fetch_val(
            query="""
                WITH delete_image as (
                    DELETE FROM image
                    WHERE image_id = :image_id RETURNING *
                ) SELECT count(*) as deleted 
                FROM delete_image;
            """,
            values={"image_id": image_id},
            column="deleted",
        )

    async def read_random_unowned_image(self, user_email: str) -> Optional[int]:
        image_id = await self._db.fetch_val(
            query="""
                WITH unowned_images as (
                    SELECT image_id, CASE rarity
                        WHEN 'Common' THEN 1
                        WHEN 'Uncommon' THEN 2
                        WHEN 'Rare' THEN 3
                        WHEN 'Epic' THEN 4
                        WHEN 'Legendary' THEN 5
                    END AS rarity_weight
                    FROM image
                    WHERE image_id NOT IN (
                        SELECT image_id from user_image ui
                        WHERE ui.user_email = :user_email
                    )
                ) SELECT image_id, -LOG(RANDOM())/rarity_weight as priority 
                FROM unowned_images
                ORDER BY priority DESC LIMIT 1;
            """,
            values={"user_email": user_email},
            column="image_id",
        )
        if image_id:
            return image_id
        raise BaseError({"code": "gacha", "description": "You already own all images"})
