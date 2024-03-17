# standard lib imports
from typing import Optional, Sequence
# module imports
from models.user_image import UserImage, UserImageCreate, UserImageUpdate
from utils import build_insert_statement, build_update_statement, filter_excluded_keys, log
# third party imports
from databases import Database


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
            values=mapped_dict, column="created"
        )

    async def read(self, limit: int, offset: int) -> Sequence[Optional[UserImage]]:
        records = await self._db.fetch_all(
            query="SELECT * FROM user_image LIMIT :limit OFFSET :offset",
            values={"limit": limit, "offset": offset}
        )
        return [UserImage(**dict(record)) for record in records]
    
    async def update(self, id: int, user_image: UserImageUpdate) -> int:
        filtered_dict = filter_excluded_keys(user_image.model_dump())
        filtered_dict["id"] = id
        update_statement = build_update_statement(mapped_dict=filtered_dict)        
        return await self._db.fetch_val(
            query=f"""
                WITH update_user_image as (
                    UPDATE user_image SET {update_statement} 
                    WHERE id = :id RETURNING *
                ) SELECT COUNT(*) as updated 
                FROM update_user_image
            """,
            values=filtered_dict, column="updated"
        )

    async def delete(self, id: int) -> int:
        return await self._db.fetch_val(
            query=f"""
                WITH delete_user_image as (
                    DELETE FROM user_image 
                    WHERE id = :id RETURNING *
                ) SELECT count(*) as deleted 
                FROM delete_user_image;
            """,
            values={"id": id}, column="deleted"
        )