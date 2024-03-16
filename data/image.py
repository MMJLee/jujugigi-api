# standard lib imports
from typing import Optional, Sequence, Mapping, Dict, Any
import json

# third party imports
from databases import Database

# module imports
from models.image import Image, ImageCreate
from utils import build_insert_statement, build_update_statement, filter_excluded_keys

class ImageData:
    def __init__(self, db: Database) -> None:
        self._db = db

    async def create(self, image: ImageCreate) -> int:
        mapped_dict = image.model_dump()
        fields_statement, values_statement = build_insert_statement(mapped_dict=mapped_dict)
        return await self._db.fetch_val(
            query=f"""
                WITH create_image AS (
                    INSERT INTO batch({fields_statement}) 
                    VALUES({values_statement}) RETURNING *
                ) SELECT COUNT(*) as created 
                FROM create_image;
            """,
            values=mapped_dict, column='created'
        )
        
    async def read(self, id: int) -> Optional[Image]:
        record = await self._db.fetch_one(
            query="SELECT * FROM image WHERE id = :id;",
            values={'id': id}
        )
        return Image(**dict(record))
    
    async def read_list(self, limit: int, offset: int) -> Sequence[Optional[Image]]:
        records = await self._db.fetch_all(
            query="SELECT * FROM image LIMIT :limit OFFSET :offset",
            values={'limit': limit, 'offset': offset}
        )
        return [Image(**dict(record)) for record in records]
    
    async def update(self, id: int, image: Image) -> int:
        filtered_dict = filter_excluded_keys(image.model_dump(), excluded_keys={'created_by', 'created_on'})
        filtered_dict['id'] = id
        
        update_statement = build_update_statement(mapped_dict=filtered_dict)

        return await self._db.fetch_val(
            query=f"""
                WITH update_image as (
                    UPDATE image SET {update_statement} 
                    WHERE id = :id RETURNING *
                ) SELECT COUNT(*) as updated 
                FROM update_image
            """,
            values=filtered_dict, column='updated'
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
            values={'id': id}, column='deleted'
        )