from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class ImageBase(BaseModel):
    subject: str = Field(..., title='subject of image')
    image_url: str = Field(..., title='url of image')

class ImageCreate(ImageBase):
    pass

class ImageUpdate(ImageBase):
    pass

class Image(ImageBase):
    id: int = Field(..., title='id of image')
    created_by: str = Field(..., title='creator of image')
    created_on: datetime = Field(..., title='creation time of image')
    updated_by: str = Field(..., title='last editor of image')
    updated_on: datetime = Field(..., title='last update time of image')
    
    class Config:
        json_schema_extra = {
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
