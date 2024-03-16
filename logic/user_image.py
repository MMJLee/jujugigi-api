from typing import Sequence, Optional

from data.user_image import UserImageData
from models.user_image import UserImage, UserImageCreate, UserImageUpdate
from datetime import datetime
from zoneinfo import ZoneInfo


class UserImageLogic:
    def __init__(self, user_image_data: UserImageData):
        self._user_image_data = user_image_data

    async def create(self, user_image: UserImageCreate, user_imagename: str) -> int:
        now = datetime.now(tz=ZoneInfo("America/Chicago"))
        user_image = UserImage(**user_image.model_dump(), created_by=user_imagename, created_on=now, updated_by=user_imagename, updated_on=now)
        return await self._user_image_data.create(user_image=user_image)

    async def read(self, id: int) -> Optional[UserImage]:
        return await self._user_image_data.read(id=id)

    async def read_list(self, limit: int, offset: int) -> Sequence[Optional[UserImage]]:
        return await self._user_image_data.read_list(limit=limit, offset=offset)

    async def update(self, user_image: UserImageUpdate, user_imagename: str) -> int:
        now = datetime.now(tz=ZoneInfo("America/Chicago"))
        user_image = UserImage(**user_image.model_dump(), updated_by=user_imagename, updated_on=now)
        return await self._user_image_data.update(user_image=user_image)

    async def delete(self, id: int) -> int:
        return await self._user_image_data.delete(id=id)