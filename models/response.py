# third party imports
from pydantic import BaseModel, Field

   
class HealthcheckResponse(BaseModel):
    status: str = Field("available", title="healthcheck status")
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "status": "available",
                }
            ]
        }
    }

class AddResponse(BaseModel):
    added: int = Field(..., title="added count")
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "added": "1",
                }
            ]
        }
    }

class UpdateResponse(BaseModel):
    updated: int = Field(..., title="updated count")
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "updated": "1",
                }
            ]
        }
    }

class DeleteResponse(BaseModel):
    deleted: int = Field(..., title="deleted count")
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "deleted": "1",
                }
            ]
        }
    }