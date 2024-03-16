from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class ImageBase(BaseModel):
    subject: str = Field(..., title='subject of image')
    url: str = Field(..., title='url of image')

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "subject": "Senate",
                    "url": "https://i.imgur.com/B8ta5Aa.jpeg"
                }
            ]
        }
    }

class ImageCreate(ImageBase):
    pass

class ImageUpdate(ImageBase):
    pass

class Image(ImageBase):
    id: int = Field(..., title='id of image')
    created_by: Optional[str] = Field(None, title='creator of user_image')
    created_on: Optional[datetime] = Field(None, title='creation time of user_image')
    updated_by: str = Field(..., title='last editor of image')
    updated_on: datetime = Field(..., title='last update time of image')
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "13",
                    "subject": "Senate",
                    "url": "https://i.imgur.com/B8ta5Aa.jpeg",
                    "created_by": "dataload",
                    "created_on": "2021-05-18 13:19:06",
                    "created_by": "dataload",
                    "updated_on": "2021-05-18 13:19:06"
                }
            ]
        }
    }
