# standard lib imports
from typing import Sequence, Optional
from datetime import datetime
from zoneinfo import ZoneInfo

# module imports
from data.user_alias import UserAliasData
from models.user_alias import UserAlias, UserAliasBase, UserAliasCreate, UserAliasUpdate


class UserAliasLogic:
    def __init__(self, user_alias_data: UserAliasData):
        self._user_alias_data = user_alias_data

    async def create(self, user_alias: UserAliasBase, user_email: str) -> int:
        user_alias = UserAliasCreate(user_alias=user_alias.user_alias, user_email=user_email, created_by=user_email, updated_by=user_email)
        return await self._user_alias_data.create(user_alias=user_alias)

    async def read(self, user_alias: Optional[str], user_email: Optional[str], limit: int, offset: int) -> Sequence[Optional[UserAlias]]:
        return await self._user_alias_data.read(user_alias=user_alias, user_email=user_email, limit=limit, offset=offset)

    async def update(self, user_alias_id: int, user_alias: UserAliasBase, user_email: str) -> int:
        now = datetime.now(tz=ZoneInfo("America/Chicago"))
        user_alias = UserAliasUpdate(**user_alias.model_dump(), updated_by=user_email, updated_on=now)
        return await self._user_alias_data.update(user_alias_id=user_alias_id, user_alias=user_alias)

    async def delete(self, user_alias_id: int) -> int:
        return await self._user_alias_data.delete(user_alias_id=user_alias_id)
