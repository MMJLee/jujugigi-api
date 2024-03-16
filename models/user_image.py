from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class UserImageBase(BaseModel):
    user_id: int = Field(..., title='id of user')
    image_id: int = Field(..., title='id of image')

class UserImageCreate(UserImageBase):
    pass

class UserImageUpdate(UserImageBase):
    pass

class UserImage(UserImageBase):
    id: int = Field(..., title='id of user_image')
    created_by: str = Field(..., title='creator of user_image')
    created_on: datetime = Field(..., title='creation time of user_image')
    updated_by: str = Field(..., title='last editor of user_image')
    updated_on: datetime = Field(..., title='last update time of user_image')
    
    class Config:
        json_schema_extra = {
            'example': {
                "id": "13",
                "owner_id": "1",
                "created_by": "dataload",
                "created_on": "2021-05-18 13:19:06",
                "created_by": "dataload",
                "updated_on": "2021-05-18 13:19:06"
            }
        }
