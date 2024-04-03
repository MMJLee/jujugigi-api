# standard lib imports
from typing import Sequence, Optional

# third party imports
from fastapi import APIRouter, Path, Query, Body, Depends, Security

# module imports
from app.api.dependencies import user_alias_logic_dependency, authorize_user
from app.logic.authorization import CRUDOperation, ResourceType
from app.logic.user_alias import UserAliasLogic
from app.models.response import AddResponse, UpdateResponse, DeleteResponse
from app.models.user_alias import UserAlias, UserAliasBase


router = APIRouter()


@router.post("", response_model=AddResponse)
async def create(
    auth_info: str = Security(
        authorize_user,
        scopes=[],
    ),
    user_alias_logic: UserAliasLogic = Depends(user_alias_logic_dependency),
    user_alias: UserAliasBase = Body(..., title="create user_alias"),
):

    user_email = auth_info
    added = await user_alias_logic.create(user_alias=user_alias, user_email=user_email)
    return AddResponse(added=added)


@router.get("", response_model=Sequence[Optional[UserAlias]])
async def read(
    auth_info: str = Security(
        authorize_user,
        scopes=[],
    ),
    user_alias_logic: UserAliasLogic = Depends(user_alias_logic_dependency),
    user_alias: Optional[str] = Query(None),
    user_email: Optional[str] = Query(None),
    limit: int = Query(1, ge=1),
    offset: int = Query(0, ge=0),
):

    _ = auth_info
    return await user_alias_logic.read(user_alias=user_alias, user_email=user_email, limit=limit, offset=offset)


@router.put("/{user_alias_id}", response_model=UpdateResponse)
async def update(
    auth_info: str = Security(
        authorize_user,
        scopes=[f"{CRUDOperation.UPDATE.value}:{ResourceType.USER_ALIAS.value}"],
    ),
    user_alias_logic: UserAliasLogic = Depends(user_alias_logic_dependency),
    user_alias_id: int = Path(..., title="user_alias id"),
    user_alias: UserAliasBase = Body(..., title="update user_alias"),
):

    user_email = auth_info
    added = await user_alias_logic.update(user_alias_id=user_alias_id, user_alias=user_alias, user_email=user_email)
    return AddResponse(added=added)


@router.delete("/{user_alias_id}", response_model=DeleteResponse)
async def delete(
    auth_info: str = Security(
        authorize_user,
        scopes=[f"{CRUDOperation.DELETE.value}:{ResourceType.USER_ALIAS.value}"],
    ),
    user_alias_logic: UserAliasLogic = Depends(user_alias_logic_dependency),
    user_alias_id: int = Path(..., title="user_alias id"),
):

    _ = auth_info
    return await user_alias_logic.delete(user_alias_id=user_alias_id)
