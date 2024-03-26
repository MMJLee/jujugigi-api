# standard lib imports
from typing import Sequence, Optional
from datetime import datetime
from zoneinfo import ZoneInfo

# module imports
from data.user_image import UserImageData
from models.user_image import UserImage, UserImageBase, UserImageCreate, UserImageUpdate, UserRankings


class UserImageLogic:
    def __init__(self, user_image_data: UserImageData):
        self._user_image_data = user_image_data

    async def create(self, user_image: UserImageBase, user_email: str) -> int:
        user_image = UserImageCreate(**user_image.model_dump(), created_by=user_email, updated_by=user_email)
        return await self._user_image_data.create(user_image=user_image)

    async def read(self, limit: int, offset: int) -> Sequence[Optional[UserImage]]:
        return await self._user_image_data.read(limit=limit, offset=offset)

    async def read_rankings(self, limit: int, offset: int) -> Sequence[Optional[UserRankings]]:
        return await self._user_image_data.read_rankings(limit=limit, offset=offset)

    async def update(self, user_image_id: int, user_image: UserImageBase, user_email: str) -> int:
        now = datetime.now(tz=ZoneInfo("America/Chicago"))
        user_image = UserImageUpdate(**user_image.model_dump(), updated_by=user_email, updated_on=now)
        return await self._user_image_data.update(user_image_id=user_image_id, user_image=user_image)

    async def delete(self, user_image_id: int) -> int:
        return await self._user_image_data.delete(user_image_id=user_image_id)
