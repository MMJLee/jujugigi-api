# standard lib imports
from typing import Optional, Sequence
# module imports
from exceptions import BaseError
from models.image import Image, ImageCreate, ImageUpdate, ImageResponse
from utils import build_insert_statement, build_update_statement, filter_excluded_keys
# third party imports
from databases import Database
from fastapi import UploadFile
from supabase import Client, StorageException
from asyncpg.exceptions import UniqueViolationError


class ImageData:
    def __init__(self, db: Database, supabase_client: Client, supabase_bucket: str, supabase_url_timeout: int) -> None:
        self._db = db
        self._supabase_client = supabase_client
        self._supabase_bucket = supabase_bucket
        self._supabase_url_timeout = supabase_url_timeout
        
    async def create(self, image: ImageCreate, image_file: UploadFile) -> int:
        try:
            self._supabase_client.storage.from_(self._supabase_bucket).upload(path=f"images/{image_file.filename}", file=image_file.file.read(), file_options={"content-type": image_file.content_type})
        except StorageException: #if dupe, continue to adding database record
            pass
        except Exception as e:
            raise BaseError({"code": "create:image", "description": e})
        
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
                values=mapped_dict, column="created"
            )
        except UniqueViolationError: #if dupe, return created
            return 1
        except Exception as e:
            raise BaseError({"code": "create:image", "description": e})
    
    async def read(self, limit: int, offset: int, id: Optional[int] = None, name: Optional[str] = None, user_email: Optional[str] = None) -> Sequence[Optional[ImageResponse]]:
        filter_statement = ""
        values = {"limit": limit, "offset": offset}
        
        if id: 
            filter_statement = "WHERE i.id = :id"
            values["id"] = id
        elif name: 
            filter_statement = "WHERE i.name = :name"
            values["name"] = name
        elif user_email: 
            filter_statement = "JOIN user_image ui ON i.id = ui.image_id WHERE ui.user_email = :user_email"
            values["user_email"] = user_email
            
        records = await self._db.fetch_all(
            query=f"""
                SELECT i.* FROM image i
                {filter_statement}
                LIMIT :limit OFFSET :offset
            """,
            values=values
        )
        images = [Image(**dict(record)) for record in records]
        paths = [f"{image.path}/{image.name}" for image in images]
        return self._supabase_client.storage.from_(self._supabase_bucket).create_signed_urls(paths=paths, expires_in=self._supabase_url_timeout)
    
    async def update(self, id: int, image: ImageUpdate) -> int:
        filtered_dict = filter_excluded_keys(image.model_dump())
        filtered_dict["id"] = id
        update_statement = build_update_statement(mapped_dict=filtered_dict)

        return await self._db.fetch_val(
            query=f"""
                WITH update_image as (
                    UPDATE image SET {update_statement} 
                    WHERE id = :id RETURNING *
                ) SELECT COUNT(*) as updated 
                FROM update_image
            """,
            values=filtered_dict, column="updated"
        )

    async def delete(self, id: int) -> int:
        return await self._db.fetch_val(
            query=f"""
                WITH delete_image as (
                    DELETE FROM image
                    WHERE id = :id RETURNING *
                ) SELECT count(*) as deleted 
                FROM delete_image;
            """,
            values={"id": id}, column="deleted"
        )
    
    async def unowned_image(self, user_email: str) -> Optional[int]:
        return await self._db.fetch_val(
            query=f"""
                WITH owned_images as (
                    SELECT image_id FROM user_image
                    WHERE user_email = :user_email
                ) SELECT i.id, -LOG(RANDOM())/rarity as priority FROM image i
                    WHERE i.id NOT IN (SELECT image_id from owned_images)
                    ORDER BY priority DESC LIMIT 1;
            """,
            values={"user_email": user_email}, 
            column="id"
        )

    async def gacha(self, user_email: str) -> Sequence[Optional[ImageResponse]]:
        id = await self._db.fetch_val(
            query=f"""
                WITH owned_images as (
                    SELECT image_id FROM user_image
                    WHERE user_email = :user_email
                ), gacha as (
                    SELECT i.id FROM image i
                    WHERE i.id NOT IN (SELECT image_id from owned_images)
                    ORDER BY RANDOM() LIMIT 1
                ), create_user_image AS (
                    INSERT INTO user_image (user_email, image_id) 
                    VALUES (:user_email, (select id from gacha)) RETURNING *
                ) SELECT image_id FROM create_user_image
            """,
            values={"user_email": user_email}, 
            column="image_id"
        )
        return await self.read(limit=1, offset=0, id=id)
    