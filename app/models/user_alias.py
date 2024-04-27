# standard lib imports
from datetime import datetime
from typing import Optional

# third party imports
from pydantic import BaseModel, Field


class UserAliasBase(BaseModel):
    user_email: Optional[str] = Field(None, title="email of user")
    user_alias: Optional[str] = Field(None, title="id of alias")
    daily_dollar: Optional[datetime] = Field(None, title="last time of daily dollar")
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_email": "example@email.com",
                    "user_alias": "alias",
                    "daily_dollar": "2021-05-18 13:19:06",
                }
            ]
        }
    }


class UserAliasCreate(UserAliasBase):
    created_by: str = Field(..., title="creator of user_alias")
    updated_by: str = Field(..., title="last editor of alias")
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_email": "example@email.com",
                    "user_alias": "alias",
                    "daily_dollar": "2021-05-18 13:19:06",
                    "created_by": "dataload",
                    "updated_by": "dataload",
                }
            ]
        }
    }


class UserAliasUpdate(UserAliasBase):
    updated_by: str = Field(..., title="last editor of user_alias")
    updated_on: datetime = Field(..., title="last update time of user_alias")
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_email": "example@email.com",
                    "user_alias": "alias",
                    "daily_dollar": "2021-05-18 13:19:06",
                    "updated_by": "dataload",
                    "updated_on": "2021-05-18 13:19:06",
                }
            ]
        }
    }


class UserAlias(UserAliasBase):
    user_alias_id: int = Field(..., title="id of user_alias")
    created_by: str = Field(..., title="creator of user_alias")
    created_on: datetime = Field(..., title="creation time of user_alias")
    updated_by: str = Field(..., title="last editor of user_alias")
    updated_on: datetime = Field(..., title="last update time of user_alias")
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_alias_id": "1",
                    "user_email": "example@email.com",
                    "user_alias": "alias",
                    "daily_dollar": "2021-05-18 13:19:06",
                    "created_by": "dataload",
                    "created_on": "2021-05-18 13:19:06",
                    "updated_by": "dataload",
                    "updated_on": "2021-05-18 13:19:06",
                }
            ]
        }
    }
