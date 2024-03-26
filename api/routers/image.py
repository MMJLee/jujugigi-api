# standard lib imports
from typing import Sequence, Optional

# third party imports
from fastapi import APIRouter, File, Path, Query, Body, Depends, Security, UploadFile

# module imports
from api.dependencies import image_logic_dependency, authorize_user
from logic.authorization import CRUDOperation, ResourceType
from logic.image import ImageLogic
from models.response import AddResponse, UpdateResponse, DeleteResponse
from models.image import ImageBase, ImageResponse


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
        scopes=[f"{CRUDOperation.CREATE.value}:{ResourceType.IMAGE.value}"],
    ),
    image_logic: ImageLogic = Depends(image_logic_dependency),
    image_id: Optional[int] = Query(None),
    user_email: Optional[str] = Query(None),
    limit: int = Query(50, ge=50),
    offset: int = Query(0, ge=0),
):

    _ = auth_info
    return await image_logic.read(image_id=image_id, user_email=user_email, limit=limit, offset=offset)


@router.put("/{image_id}", response_model=UpdateResponse)
async def update(
    auth_info: str = Security(
        authorize_user,
        scopes=[f"{CRUDOperation.UPDATE.value}:{ResourceType.IMAGE.value}"],
    ),
    image_logic: ImageLogic = Depends(image_logic_dependency),
    image_id: int = Path(..., title="image_id"),
    image: ImageBase = Body(..., title="update image"),
):

    user_email = auth_info
    added = await image_logic.update(image_id=image_id, image=image, user_email=user_email)
    return AddResponse(added=added)


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
    return await image_logic.delete(image_id=image_id)


@router.get("/gacha", response_model=Sequence[Optional[ImageResponse]])
async def gacha(
    auth_info: str = Security(
        authorize_user,
        scopes=[f"{CRUDOperation.READ.value}:{ResourceType.IMAGE.value}"],
    ),
    user_image_logic: ImageLogic = Depends(image_logic_dependency),
):

    user_email = auth_info
    return await user_image_logic.gacha(user_email=user_email)
