# standard lib imports
from datetime import datetime
from typing import Optional

# third party imports
from pydantic import BaseModel, Field


class UserImageBase(BaseModel):
    user_email: Optional[str] = Field(None, title="email of user")
    image_id: int = Field(..., title="id of image")
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_email": "example@email.com",
                    "image_id": "1",
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
                    "updated_by": "dataload",
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
                    "updated_on": "2021-05-18 13:19:06",
                }
            ]
        }
    }


class UserImage(UserImageBase):
    user_image_id: int = Field(..., title="id of user_image")
    created_by: str = Field(..., title="creator of user_image")
    created_on: datetime = Field(..., title="creation time of user_image")
    updated_by: str = Field(..., title="last editor of user_image")
    updated_on: datetime = Field(..., title="last update time of user_image")
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_image_id": "1",
                    "user_email": "example@email.com",
                    "image_id": "1",
                    "created_by": "dataload",
                    "created_on": "2021-05-18 13:19:06",
                    "updated_by": "dataload",
                    "updated_on": "2021-05-18 13:19:06",
                }
            ]
        }
    }


class UserRankings(BaseModel):
    user_alias: str = Field(..., title="alias of user")
    common_count: int = Field(..., title="count of common images")
    uncommon_count: int = Field(..., title="count of uncommon images")
    rare_count: int = Field(..., title="count of rare images")
    epic_count: int = Field(..., title="count of epic images")
    unique_count: int = Field(..., title="count of unique images")
    total_count: int = Field(..., title="count of total images")
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_alias": "alias",
                    "common_count": "1",
                    "uncommon_count": "1",
                    "rare_count": "1",
                    "epic_count": "1",
                    "unique_count": "1",
                    "total_count": "1",
                }
            ]
        }
    }
