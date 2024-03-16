# standard lib imports
from typing import Sequence, Tuple, Optional

# third party imports
from fastapi import APIRouter, Path, Query, Body, Depends, Security

# module imports
from api.dependencies import image_logic_dependency, authorize_user
from logic.image import ImageLogic
from logic.authorization import CRUDOperation, ResourceType, AuthorizationLogic
from models.image import Image, ImageCreate, ImageUpdate
from models.response import AddResponse, UpdateResponse, DeleteResponse

router = APIRouter()

@router.post('', response_model=AddResponse)
async def create(auth_info: str = Security(authorize_user, scopes=[f'{CRUDOperation.CREATE}:{ResourceType.IMAGE}']),
                  image_logic: ImageLogic = Depends(image_logic_dependency), image: ImageCreate = Body(..., title='create image')):

    imagename = auth_info
    added = await image_logic.create(image=image, imagename=imagename)
    return AddResponse(added=added)

@router.get('/{id}', response_model=Optional[Image])
async def read(auth_info: str = Security(authorize_user, scopes=[f'{CRUDOperation.DELETE}:{ResourceType.IMAGE}']),
                   image_logic: ImageLogic = Depends(image_logic_dependency), id: int = Path(..., title="image id")):
    
    _ = auth_info
    return await image_logic.read(id=id)

@router.get('', response_model=Sequence[Optional[Image]])
async def read_list(auth_info: str = Security(authorize_user, scopes=[f'{CRUDOperation.READ}:{ResourceType.IMAGE}']),
                   image_logic: ImageLogic = Depends(image_logic_dependency), limit: int = Query(100, ge=50), offset: int = Query(0, ge=0)):
    
    _ = auth_info
    return await image_logic.read_list(limit=limit, offset=offset)

@router.put('/{id}', response_model=UpdateResponse)
async def update(auth_info: str = Security(authorize_user, scopes=[f'{CRUDOperation.UPDATE}:{ResourceType.IMAGE}']),
                  image_logic: ImageLogic = Depends(image_logic_dependency), image: ImageUpdate = Body(..., title='update image')):

    imagename = auth_info
    added = await image_logic.create(image=image, imagename=imagename)
    return AddResponse(added=added)

@router.delete('/{id}', response_model=DeleteResponse)
async def delete(auth_info: str = Security(authorize_user, scopes=[f'{CRUDOperation.DELETE}:{ResourceType.IMAGE}']),
                   image_logic: ImageLogic = Depends(image_logic_dependency), id: int = Path(..., title="image id")):
    
    _ = auth_info
    return await image_logic.delete(id=id)


@router.get('/1')
async def reasd(auth_info: str = Security(authorize_user, scopes=[f'{CRUDOperation.DELETE}:{ResourceType.IMAGE}']),
                   image_logic: ImageLogic = Depends(image_logic_dependency), id: int = Path(..., title="image id")):
    
    _ = auth_info
    return await image_logic.read(id=id)