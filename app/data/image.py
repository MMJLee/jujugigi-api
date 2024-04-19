# standard lib imports
from typing import Any, Optional, Sequence

# third party imports
from databases import Database
from fastapi import UploadFile
from supabase import Client, StorageException
from asyncpg.exceptions import UniqueViolationError

# module imports
from app.exceptions import BaseError
from app.models.image import ImageCreate, ImageResponse, ImageUpdate
from app.utils import build_insert_statement, build_update_statement


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
        except StorageException as e:
            raise BaseError({"code": "create:supabase", "description": e}) from e
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
        self,
        image_id: Optional[int] = None,
        user_email: Optional[str] = None,
        user_alias: Optional[str] = None,
        user_image_id: Optional[str] = None,
        opened: Optional[bool] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Sequence[Optional[ImageResponse]]:

        filter_statement = "JOIN user_image ui ON i.image_id = ui.image_id "
        values = {"limit": limit, "offset": offset}

        if image_id:
            filter_statement = """
                WHERE i.image_id = :image_id
            """
            values["image_id"] = image_id

        elif user_image_id:
            filter_statement += """
                WHERE ui.user_image_id = :user_image_id
            """
            values["user_image_id"] = user_image_id

        elif user_email:
            filter_statement += """
                WHERE ui.user_email = :user_email
            """
            values["user_email"] = user_email

        elif user_alias:
            filter_statement += """
                JOIN user_alias ua ON ui.user_email = ua.user_email 
                WHERE ua.user_alias ILIKE :user_alias
            """
            values["user_alias"] = user_alias

        if opened is not None:
            filter_statement += " AND ui.opened = :opened"
            values["opened"] = opened

        records = await self._db.fetch_all(
            query=f"""
                SELECT i.path, i.file_name, i.description, i.rarity
                FROM image i
                {filter_statement}
                ORDER BY ui.created_on DESC
                LIMIT :limit OFFSET :offset
            """,
            values=values,
        )
        image_response = []
        if records:
            paths = [f"{record.path}/{record.file_name}" for record in records]
            image_details = self._supabase_client.storage.from_(self._supabase_bucket).create_signed_urls(paths=paths, expires_in=self._supabase_url_timeout)
            for i, record in enumerate(records):
                image_response.append(ImageResponse(**dict(record), signedURL=image_details[i].get("signedURL")))
        return image_response

    async def read_all(self) -> Sequence[Optional[Any]]:
        images = self._supabase_client.storage.from_(self._supabase_bucket).list("images")
        return [image["name"] for image in images]

    async def update(self, image: ImageUpdate, image_file: UploadFile) -> int:
        try:
            self._supabase_client.storage.from_(self._supabase_bucket).update(
                path=f"images/{image_file.filename}", file=image_file.file.read(), file_options={"content-type": image_file.content_type, "upsert": "true"}
            )
        except StorageException as e:
            raise BaseError({"code": "update:supabase", "description": e}) from e
        except Exception as e:
            raise BaseError({"code": "update:image", "description": e}) from e

        mapped_dict = image.model_dump()
        update_statement = build_update_statement(mapped_dict=mapped_dict)

        try:
            return await self._db.fetch_val(
                query=f"""
                    WITH update_image as (
                    UPDATE image SET {update_statement}
                        WHERE file_name = :file_name RETURNING *
                    ) SELECT COUNT(*) as updated 
                    FROM update_image
                """,
                values=mapped_dict,
                column="updated",
            )
        except Exception as e:
            raise BaseError({"code": "update:image", "description": e}) from e

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
                SELECT i.image_id, -LOG(RANDOM())/i.rarity as priority 
                FROM image i WHERE i.image_id NOT IN (
                    SELECT image_id FROM user_image ui WHERE ui.user_email = :user_email
                ) ORDER BY priority DESC LIMIT 1;
            """,
            values={"user_email": user_email},
            column="image_id",
        )
        if image_id:
            return image_id
        raise BaseError({"code": "gacha", "description": "You already own all images"})
