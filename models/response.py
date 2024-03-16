from pydantic import BaseModel, Field

        
class HealthcheckResponse(BaseModel):
    status: str = Field('available', title='healthcheck status')

    class Config:
        json_schema_extra = {
            'example': {
                'status': 'available',
            }
        }

class AddResponse(BaseModel):
    added: int = Field(..., title='added count')
    class Config:
        json_schema_extra = {
            'example': {
                'added': '1',
            }
        }

class UpdateResponse(BaseModel):
    updated: int = Field(..., title='updated count')
    class Config:
        json_schema_extra = {
            'example': {
                'updated': 1,
            }
        }

class DeleteResponse(BaseModel):
    deleted: int = Field(..., title='deleted count')
    class Config:
        json_schema_extra = {
            'example': {
                'deleted': 1,
            }
        }