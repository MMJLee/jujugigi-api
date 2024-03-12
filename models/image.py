from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class ImageBase(BaseModel):
    subject: str = Field(...)
    image_url: str = Field(...)

class ImageCreate(ImageBase):
    pass

class Image(ImageBase):
    id: int = Field(...)
    created_by: str = Field(...)
    created_on: datetime = Field(...)
    updated_by: str = Field(...)
    updated_on: datetime = Field(...)
    
    class Config:
        schema_extra = {
            'example': {
                "id": "13",
                "subject": "Senate",
                "image_url": "https://i.imgur.com/B8ta5Aa.jpeg",
                "created_by": "dataload",
                "created_on": "2021-05-18 13:19:06",
                "created_by": "dataload",
                "updated_on": "2021-05-18 13:19:06"
            }
        }
