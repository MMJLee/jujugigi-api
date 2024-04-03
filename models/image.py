# standard lib imports
from datetime import datetime
from typing import Optional, Any

# third party imports
from pydantic import BaseModel, Field


class ImageBase(BaseModel):
    subject: str = Field(..., title="subject of image")
    path: str = Field(..., title="path of image")
    file_name: str = Field(..., title="file_name of image")
    description: str = Field(..., title="description of image")
    rarity_id: int = Field(..., title="rarity_id of image")  # 1-5: common, uncommon, rare, epic, unique
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "subject": "Geneva",
                    "path": "images",
                    "file_name": "G1_couch_potato.jpeg",
                    "description": "couch potato",
                    "rarity_id": "1",
                }
            ]
        }
    }


class ImageCreate(ImageBase):
    created_by: str = Field(..., title="creator of user_image")
    updated_by: str = Field(..., title="last editor of image")
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "subject": "Geneva",
                    "path": "images",
                    "file_name": "G1_couch_potato.jpeg",
                    "description": "couch potato",
                    "rarity_id": "1",
                    "created_by": "dataload",
                    "updated_by": "dataload",
                }
            ]
        }
    }


class ImageUpdate(ImageBase):
    updated_by: str = Field(..., title="last editor of image")
    updated_on: datetime = Field(..., title="last update time of image")
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "subject": "Geneva",
                    "path": "images",
                    "file_name": "G1_couch_potato.jpeg",
                    "description": "couch potato",
                    "rarity_id": "1",
                    "updated_by": "dataload",
                    "updated_on": "2021-05-18 13:19:06",
                }
            ]
        }
    }


class Image(ImageBase):
    image_id: int = Field(..., title="id of image")
    created_by: str = Field(..., title="creator of user_image")
    created_on: datetime = Field(..., title="creation time of user_image")
    updated_by: str = Field(..., title="last editor of image")
    updated_on: datetime = Field(..., title="last update time of image")
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "image_id": "1",
                    "subject": "Geneva",
                    "path": "images",
                    "file_name": "G1_couch_potato.jpeg",
                    "description": "couch potato",
                    "rarity_id": "1",
                    "created_by": "dataload",
                    "created_on": "2021-05-18 13:19:06",
                    "updated_by": "dataload",
                    "updated_on": "2021-05-18 13:19:06",
                }
            ]
        }
    }


class ImageURL(BaseModel):
    error: Optional[Any] = Field(None, title="error of response")
    path: str = Field(..., title="path of file including file_name")
    signedURL: str = Field(..., title="signed url of file")
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "error": None,
                    "path": "images/G1_couch_potato.jpeg",
                    "signedURL": "https://efexmishlqcwakuvktjb.supabase.co/storage/v1/object/sign/jujugigi/images/image-1.jpg?token=eyJhbGciOiJIUzI1Ni",
                }
            ]
        }
    }


class ImageResponse(BaseModel):
    path: str = Field(..., title="path of image")
    file_name: str = Field(..., title="file_name of image")
    description: str = Field(..., title="description of image")
    rarity_name: str = Field(..., title="rarity of image")  # common, uncommon, rare, epic, unique
    signedURL: str = Field(..., title="signed url of file")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "path": "images",
                    "file_name": "G1_couch_potato.jpeg",
                    "description": "couch potato",
                    "rarity": "1",
                    "signedURL": "https://efexmishlqcwakuvktjb.supabase.co/storage/v1/object/sign/jujugigi/images/image-1.jpg?token=eyJhbGciOiJIUzI1N2",
                }
            ]
        }
    }
