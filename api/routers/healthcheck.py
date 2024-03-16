# third party imports 
from fastapi import APIRouter
import os 
# module imports
from models.response import HealthcheckResponse

router = APIRouter()

@router.get('', response_model=HealthcheckResponse)
async def healthcheck():
    return HealthcheckResponse()

