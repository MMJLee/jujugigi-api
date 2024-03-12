from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class UserImageBase(BaseModel):
    user_id: int = Field(...)
    image_id: int = Field(...)

class UserImageCreate(UserImageBase):
    pass

class UserImage(UserImageBase):
    id: int = Field(...)
    created_by: str = Field(...)
    created_on: datetime = Field(...)
    updated_by: str = Field(...)
    updated_on: datetime = Field(...)
    
    class Config:
        schema_extra = {
            'example': {
                "id": "13",
                "owner_id": "1",
                "created_by": "dataload",
                "created_on": "2021-05-18 13:19:06",
                "created_by": "dataload",
                "updated_on": "2021-05-18 13:19:06"
            }
        }
