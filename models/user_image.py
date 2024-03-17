# standard lib imports
from datetime import datetime
# third party imports
from pydantic import BaseModel, Field


class UserImageBase(BaseModel):
    user_email: str = Field(..., title="email of user")
    image_id: int = Field(..., title="id of image")
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_email": "example@email.com",
                    "image_id": "1"
                }
            ]
        }
    }

class UserImageCreate(UserImageBase):
    created_by: str = Field(..., title="creator of user_image")
    updated_by: str = Field(..., title="last editor of image")
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_email": "example@email.com",
                    "image_id": "1",
                    "created_by": "dataload",
                    "updated_by": "dataload"
                }
            ]
        }
    }
        
class UserImageUpdate(UserImageBase):
    updated_by: str = Field(..., title="last editor of user_image")
    updated_on: datetime = Field(..., title="last update time of user_image")
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_email": "example@email.com",
                    "image_id": "1",
                    "updated_by": "dataload",
                    "updated_on": "2021-05-18 13:19:06"
                }
            ]
        }
    }
    
class UserImage(UserImageBase):
    id: int = Field(..., title="id of user_image")
    created_by: str = Field(..., title="creator of user_image")
    created_on: datetime = Field(..., title="creation time of user_image")
    updated_by: str = Field(..., title="last editor of user_image")
    updated_on: datetime = Field(..., title="last update time of user_image")
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "1",
                    "user_email": "example@email.com",
                    "image_id": "1",
                    "created_by": "dataload",
                    "created_on": "2021-05-18 13:19:06",
                    "updated_by": "dataload",
                    "updated_on": "2021-05-18 13:19:06"
                }
            ]
        }
    }