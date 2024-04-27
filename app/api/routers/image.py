# standard lib imports
from typing import Sequence, Optional

# third party imports
from fastapi import APIRouter, File, Path, Query, Body, Depends, Security, UploadFile

# module imports
from app.api.dependencies import image_logic_dependency, authorize_user
from app.logic.authorization import CRUDOperation, ResourceType
from app.logic.image import ImageLogic
from app.models.response import AddResponse, UpdateResponse, DeleteResponse
from app.models.image import ImageBase, ImageResponse


router = APIRouter()


@router.post("", response_model=AddResponse)
async def create(
    auth_info: str = Security(
        authorize_user,
        scopes=[f"{CRUDOperation.CREATE.value}:{ResourceType.IMAGE.value}"],
    ),
    image_logic: ImageLogic = Depends(image_logic_dependency),
    image_file: UploadFile = File(..., title="image file"),
):

    user_email = auth_info
    added = await image_logic.create(image_file=image_file, user_email=user_email)
    return AddResponse(added=added)


@router.post("/bulk", response_model=AddResponse)
async def bulk_create(
    auth_info: str = Security(
        authorize_user,
        scopes=[f"{CRUDOperation.CREATE.value}:{ResourceType.IMAGE.value}"],
    ),
    image_logic: ImageLogic = Depends(image_logic_dependency),
    image_files: Sequence[UploadFile] = File(..., title="image files"),
):

    user_email = auth_info
    added = await image_logic.bulk_create(image_files=image_files, user_email=user_email)
    return AddResponse(added=added)


@router.get("", response_model=Sequence[Optional[ImageResponse]])
async def read(
    auth_info: str = Security(
        authorize_user,
        scopes=[],
    ),
    image_logic: ImageLogic = Depends(image_logic_dependency),
    user_email: Optional[str] = Query(None),
    user_alias: Optional[str] = Query(None),
    opened: Optional[bool] = Query(None),
    limit: int = Query(50, ge=1),
    offset: int = Query(0, ge=0),
):

    _ = auth_info
    return await image_logic.read(user_email=user_email, user_alias=user_alias, opened=opened, limit=limit, offset=offset)


@router.put("/", response_model=UpdateResponse)
async def update(
    auth_info: str = Security(
        authorize_user,
        scopes=[f"{CRUDOperation.UPDATE.value}:{ResourceType.IMAGE.value}"],
    ),
    image_logic: ImageLogic = Depends(image_logic_dependency),
    image: ImageBase = Body(..., title="update image"),
):

    user_email = auth_info
    updated = await image_logic.update(image=image, user_email=user_email)
    return UpdateResponse(updated=updated)


@router.delete("/{image_id}", response_model=DeleteResponse)
async def delete(
    auth_info: str = Security(
        authorize_user,
        scopes=[f"{CRUDOperation.DELETE.value}:{ResourceType.IMAGE.value}"],
    ),
    image_logic: ImageLogic = Depends(image_logic_dependency),
    image_id: int = Path(..., title="image_id"),
):

    _ = auth_info
    deleted = await image_logic.delete(image_id=image_id)
    return DeleteResponse(deleted=deleted)


@router.put("/open", response_model=Sequence[Optional[ImageResponse]])
async def open_image(
    auth_info: str = Security(
        authorize_user,
        scopes=[],
    ),
    image_logic: ImageLogic = Depends(image_logic_dependency),
):

    user_email = auth_info
    return await image_logic.open_image(user_email=user_email)


@router.post("/dd", response_model=bool)
async def daily_dollar(
    auth_info: str = Security(
        authorize_user,
        scopes=[],
    ),
    image_logic: ImageLogic = Depends(image_logic_dependency),
):

    user_email = auth_info
    added = await image_logic.daily_dollar(user_email=user_email)
    return bool(added)
