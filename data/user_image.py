# standard lib imports
from typing import Optional, Sequence, Mapping, Dict, Any
import json

# third party imports
from databases import Database

# module imports
from models.user_image import UserImage, UserImageCreate
from utils import build_insert_statement, build_update_statement, filter_excluded_keys

class UserImageData:
    def __init__(self, db: Database) -> None:
        self._db = db

    async def create(self, user_image: UserImageCreate) -> int:
        mapped_dict = self._map_model_to_dict(user_image=user_image)
        fields_statement, values_statement = build_insert_statement(mapped_dict=mapped_dict)
        return await self._db.fetch_val(
            query=f"""
                WITH create_user_image AS (
                    INSERT INTO batch({fields_statement}) 
                    VALUES({values_statement}) RETURNING *
                ) SELECT COUNT(*) as created 
                FROM create_user_image;
            """,
            values=mapped_dict, column='created'
        )
        
    async def read(self, id: int) -> Optional[UserImage]:
        record = await self._db.fetch_one(
            query="SELECT * FROM user_image WHERE id = :id;",
            values={'id': id}
        )
        return UserImage(**dict(record))
    
    async def read_list(self, limit: int, offset: int) -> Sequence[Optional[UserImage]]:
        record = await self._db.fetch_all(
            query="SELECT * FROM user_image LIMIT :limit OFFSET :offset",
            values={'limit': limit, 'offset': offset}
        )
        return [UserImage(**dict(record)) for record in UserImage]
    
    async def update(self, id: int, user_image: UserImage) -> int:
        # build dictionary for performing update
        mapped_dict = self._map_model_to_dict(user_image=user_image)
        # filter out excluded update keys
        filtered_dict = filter_excluded_keys(
            mapped_dict=mapped_dict,
            excluded_keys={'created_by', 'created_on'}
        )
        # explicity setting the id value
        filtered_dict['id'] = id
        
        # create update statement
        update_statement = build_update_statement(mapped_dict=filtered_dict)

        return await self._db.fetch_val(
            query=f"""
                WITH update_user_image as (
                    UPDATE user_image SET {update_statement} 
                    WHERE id = :id RETURNING *
                ) SELECT COUNT(*) as updated 
                FROM update_user_image
            """,
            values=filtered_dict, column='updated'
        )

    async def delete(self, id: int) -> int:
        return await self._db.fetch_val(
            query=f"""
                WITH delete_user_image as (
                    DELETE FROM user_image 
                    WHERE id = :id RETURNING *
                ) SELECT count(*) as deleted 
                FROMdelete_user_image;
            """,
            values={'id': id}, column='deleted'
        )