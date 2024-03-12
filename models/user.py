from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class UserBase(BaseModel):
    email: str = Field(...)
    password: Optional[str] = Field(None)
    
class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int = Field(...)
    is_active: bool = Field(False)
    created_by: str = Field(...)
    created_on: datetime = Field(...)
    updated_by: str = Field(...)
    updated_on: datetime = Field(...)
    
    class Config:
        schema_extra = {
            'example': {
                "id": "1",
                "email": "example@email.com",
                'is_active': "true",
                "created_by": "dataload",
                "created_on": "2021-05-18 13:19:06",
                "created_by": "dataload",
                "updated_on": "2021-05-18 13:19:06"
            }
        }