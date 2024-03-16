# standard lib imports
from typing import Sequence, Tuple, Optional

# third party imports
from fastapi import APIRouter, Path, Query, Body, Depends, Security

# module imports
from api.dependencies import user_image_logic_dependency, authorize_user
from logic.user_image import UserImageLogic
from logic.authorization import CRUDOperation, ResourceType
from models.user_image import UserImage, UserImageCreate, UserImageUpdate
from models.response import AddResponse, UpdateResponse, DeleteResponse

router = APIRouter()

@router.post('', response_model=AddResponse)
async def create(auth_info: str = Security(authorize_user, scopes=[f'{CRUDOperation.CREATE}:{ResourceType.USER_IMAGE}']),
                  user_image_logic: UserImageLogic = Depends(user_image_logic_dependency), user_image: UserImageCreate = Body(..., title='create user_image')):

    user_imagename = auth_info
    added = await user_image_logic.create(user_image=user_image, user_imagename=user_imagename)
    return AddResponse(added=added)

@router.get('/{id}', response_model=Optional[UserImage])
async def read(auth_info: str = Security(authorize_user, scopes=[f'{CRUDOperation.DELETE}:{ResourceType.USER_IMAGE}']),
                   user_image_logic: UserImageLogic = Depends(user_image_logic_dependency), id: int = Path(..., title="user_image id")):
    
    _ = auth_info
    return await user_image_logic.read(id=id)

@router.get('', response_model=Sequence[Optional[UserImage]])
async def read_list(auth_info: str = Security(authorize_user, scopes=[f'{CRUDOperation.READ}:{ResourceType.USER_IMAGE}']),
                   user_image_logic: UserImageLogic = Depends(user_image_logic_dependency), limit: int = Query(100, ge=50), offset: int = Query(0, ge=0)):
    
    _ = auth_info
    return await user_image_logic.read_list(limit=limit, offset=offset)

@router.put('/{id}', response_model=UpdateResponse)
async def update(auth_info: str = Security(authorize_user, scopes=[f'{CRUDOperation.UPDATE}:{ResourceType.USER_IMAGE}']),
                  user_image_logic: UserImageLogic = Depends(user_image_logic_dependency), user_image: UserImageUpdate = Body(..., title='update user_image')):

    user_imagename = auth_info
    added = await user_image_logic.create(user_image=user_image, user_imagename=user_imagename)
    return AddResponse(added=added)

@router.delete('/{id}', response_model=DeleteResponse)
async def delete(auth_info: str = Security(authorize_user, scopes=[f'{CRUDOperation.DELETE}:{ResourceType.USER_IMAGE}']),
                   user_image_logic: UserImageLogic = Depends(user_image_logic_dependency), id: int = Path(..., title="user_image id")):
    
    _ = auth_info
    return await user_image_logic.delete(id=id)