# standard lib imports
from typing import Sequence, Optional

# third party imports
from fastapi import APIRouter, Path, Query, Body, Depends, Security

# module imports
from app.api.dependencies import user_image_logic_dependency, authorize_user
from app.logic.authorization import CRUDOperation, ResourceType
from app.logic.user_image import UserImageLogic
from app.models.response import AddResponse, UpdateResponse, DeleteResponse
from app.models.user_image import UserImage, UserImageBase, UserRankings


router = APIRouter()


@router.post("", response_model=AddResponse)
async def create(
    auth_info: str = Security(
        authorize_user,
        scopes=[f"{CRUDOperation.CREATE.value}:{ResourceType.USER_IMAGE.value}"],
    ),
    user_image_logic: UserImageLogic = Depends(user_image_logic_dependency),
    user_image: UserImageBase = Body(..., title="create user_image"),
):

    user_email = auth_info
    added = await user_image_logic.create(user_image=user_image, user_email=user_email)
    return AddResponse(added=added)


@router.get("", response_model=Sequence[Optional[UserImage]])
async def read(
    auth_info: str = Security(
        authorize_user,
        scopes=[],
    ),
    user_image_logic: UserImageLogic = Depends(user_image_logic_dependency),
    limit: int = Query(50, ge=50),
    offset: int = Query(0, ge=0),
):

    _ = auth_info
    return await user_image_logic.read(limit=limit, offset=offset)


@router.get("/rankings", response_model=Sequence[Optional[UserRankings]])
async def read_rankings(
    user_image_logic: UserImageLogic = Depends(user_image_logic_dependency),
    limit: int = Query(10, ge=10),
    offset: int = Query(0, ge=0),
):

    return await user_image_logic.read_rankings(limit=limit, offset=offset)


@router.put("/{user_image_id}", response_model=UpdateResponse)
async def update(
    auth_info: str = Security(
        authorize_user,
        scopes=[f"{CRUDOperation.UPDATE.value}:{ResourceType.USER_IMAGE.value}"],
    ),
    user_image_logic: UserImageLogic = Depends(user_image_logic_dependency),
    user_image_id: int = Path(..., title="user_image id"),
    user_image: UserImageBase = Body(..., title="update user_image"),
):

    user_email = auth_info
    added = await user_image_logic.update(user_image_id=user_image_id, user_image=user_image, user_email=user_email)
    return AddResponse(added=added)


@router.delete("/{user_image_id}", response_model=DeleteResponse)
async def delete(
    auth_info: str = Security(
        authorize_user,
        scopes=[f"{CRUDOperation.DELETE.value}:{ResourceType.USER_IMAGE.value}"],
    ),
    user_image_logic: UserImageLogic = Depends(user_image_logic_dependency),
    user_image_id: int = Path(..., title="user_image id"),
):

    _ = auth_info
    return await user_image_logic.delete(user_image_id=user_image_id)
