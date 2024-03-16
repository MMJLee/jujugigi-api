# standard lib imports
from typing import Optional, Sequence, Mapping, Dict, Any
import json

# third party imports
from databases import Database

# module imports
from models.user_image import UserImage, UserImageCreate
from utils import build_insert_stmts, build_update_stmt, filter_excluded_keys, map_dictionary

class UserImageData:
    def __init__(self, db: Database) -> None:
        self._db = db

    def make_dict(self, record: Optional[Mapping[Any, Any]]) -> Optional[Any]:
        dict = {}
        for key in record:
            if record[key]:
                map = {key: record[key]}
            else:
                map = {key: ''}
            dict.update(map)
        return dict


    # def _map_record_to_model(self, record: Optional[Mapping[Any, Any]]) -> Optional[Any]:
    #     if not record:
    #         return None

    #     mapped_dict = map_dictionary(
    #         to_be_mapped=dict(record),
    #         key_map=BillingBatchData.field_mapping,
    #         reverse=True
    #     )

    #     for field in BillingBatchData.json_fields:
    #         mapped_dict[field] = json.loads(mapped_dict.get(field) or '{}')

    #     return User(**mapped_dict)

    # def _map_model_to_dict(self, user_image: User) -> Dict[str, Any]:
    #     mapped_dict = map_dictionary(
    #         to_be_mapped=billing_batch.dict(),
    #         key_map=BillingBatchData.field_mapping,
    #         json_fields=BillingBatchData.json_fields
    #     )

    #     return mapped_dict

    async def create(self, user_image: UserImageCreate) -> int:
        mapped_dict = self._map_model_to_dict(user_image=user_image)
        fields_stmt, values_stmt = build_insert_stmts(mapped_dict=mapped_dict)
        return await self._db.fetch_val(
            query=f"WITH create_user_image AS (INSERT INTO batch({fields_stmt}) VALUES({values_stmt}) RETURNING *) SELECT COUNT(*) as created FROM create_user_image;",
            values=mapped_dict, column='created'
        )
        
    async def read(self, id: int) -> Optional[UserImage]:
        record = await self._db.fetch_one(
            query="SELECT * FROM user_image WHERE id = :id;",
            values={'id': id}
        )
        return self._map_record_to_model(record=record)
    
    async def read_list(self, limit: int, offset: int) -> Sequence[Optional[UserImage]]:
        record = await self._db.fetch_all(
            query="SELECT * FROM user_image LIMIT :limit OFFSET: offset",
            values={'limit': limit, 'offset': offset}
        )
        return self._map_record_to_model(record=record)
    
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
        update_stmt = build_update_stmt(mapped_dict=filtered_dict)

        return await self._db.fetch_val(
            query=f"WITH update_user_image as (UPDATE user_image SET {update_stmt} WHERE id = :id RETURNING *) SELECT COUNT(*) as updated from update_user_image",
            values=filtered_dict, column='updated'
        )

    async def delete(self, id: int) -> int:
        return await self._db.fetch_val(
            query=f"WITH delete_user_image as (DELETE FROM user_image WHERE id = :id RETURNING *) SELECT count(*) as deleted from delete_user_image;",
            values={'id': id}, column='deleted'
        )