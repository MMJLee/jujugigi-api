# standard lib imports
from datetime import datetime
from typing import Optional, Any
# third party imports
from pydantic import BaseModel, Field


class ImageBase(BaseModel):
    subject: str = Field(..., title="subject of image")
    path: str = Field(..., title="path of image")
    name: str = Field(..., title="name of image")
    mime_type: str = Field(..., title="mime type of image")
    rarity: int = Field(..., title="rarity of image")
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "subject": "Geneva",
                    "path": "images",
                    "name": "G1_couch_potato.jpeg",
                    "mime_type": "image/jpeg",
                    "rarity": "1",
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
                    "name": "G1_couch_potato.jpeg",
                    "mime_type": "image/jpeg",
                    "rarity": "1",
                    "created_by": "dataload",
                    "updated_by": "dataload"
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
                    "id": "1",
                    "subject": "Geneva",
                    "path": "images",
                    "name": "G1_couch_potato.jpeg",
                    "mime_type": "image/jpeg",
                    "rarity": "1",
                    "updated_by": "dataload",
                    "updated_on": "2021-05-18 13:19:06"
                }
            ]
        }
    }
    
class Image(ImageBase):
    id: int = Field(..., title="id of image")
    created_by: str = Field(..., title="creator of user_image")
    created_on: datetime = Field(..., title="creation time of user_image")
    updated_by: str = Field(..., title="last editor of image")
    updated_on: datetime = Field(..., title="last update time of image")
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "1",
                    "subject": "Geneva",
                    "path": "images",
                    "name": "G1_couch_potato.jpeg",
                    "mime_type": "image/jpeg",
                    "rarity": "1",
                    "created_by": "dataload",
                    "created_on": "2021-05-18 13:19:06",
                    "updated_by": "dataload",
                    "updated_on": "2021-05-18 13:19:06"
                }
            ]
        }
    }
    
class ImageResponse(BaseModel):
    error: Optional[Any] = Field(None, title="error of response")
    path: str = Field(..., title="path of file including name")
    signedURL: str = Field(..., title="signed url of file")
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "error": None, 
                    "path": "images/G1_couch_potato.jpeg", 
                    "signedURL": "https://efexmishlqcwakuvktjb.supabase.co/storage/v1/object/sign/jujugigi/images/image-1.jpg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJqdWp1Z2lnaS9pbWFnZXMvaW1hZ2UtMS5qcGciLCJpYXQiOjE3MTA2NTMyMTMsImV4cCI6MTcxMDY1MzUxM30.pvr_4Pek75E_bme9YK0PRWM4AIGyaoVZgsFQcdlQFYM"
                }
            ]
        }
    }