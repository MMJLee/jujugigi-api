from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class UserImageBase(BaseModel):
    email: str = Field(..., title='email of user')
    image_id: int = Field(..., title='id of image')
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "13",
                    "email": "example@email.com",
                    "image_id": "1",
                }
            ]
        }
    }


class UserImageCreate(UserImageBase):
    pass

class UserImageUpdate(UserImageBase):
    pass

class UserImage(UserImageBase):
    id: int = Field(..., title='id of user_image')
    created_by: Optional[str] = Field(None, title='creator of user_image')
    created_on: Optional[datetime] = Field(None, title='creation time of user_image')
    updated_by: str = Field(..., title='last editor of user_image')
    updated_on: datetime = Field(..., title='last update time of user_image')
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "13",
                    "email": "example@email.com",
                    "image_id": "1",
                    "created_by": "dataload",
                    "created_on": "2021-05-18 13:19:06",
                    "created_by": "dataload",
                    "updated_on": "2021-05-18 13:19:06"
                }
            ]
        }
    }