from typing import Sequence, Optional

from data.image import ImageData
from models.image import Image, ImageCreate, ImageUpdate
from datetime import datetime
from zoneinfo import ZoneInfo


class ImageLogic:
    def __init__(self, image_data: ImageData):
        self._image_data = image_data

    async def create(self, image: ImageCreate, imagename: str) -> int:
        now = datetime.now(tz=ZoneInfo("America/Chicago"))
        image = Image(**image.model_dump(), created_by=imagename, created_on=now, updated_by=imagename, updated_on=now)
        return await self._image_data.create(image=image)

    async def read(self, id: int) -> Optional[Image]:
        return await self._image_data.read(id=id)

    async def read_list(self, limit: int, offset: int) -> Sequence[Optional[Image]]:
        return await self._image_data.read_list(limit=limit, offset=offset)

    async def update(self, image: ImageUpdate, imagename: str) -> int:
        now = datetime.now(tz=ZoneInfo("America/Chicago"))
        image = Image(**image.model_dump(), updated_by=imagename, updated_on=now)
        return await self._image_data.update(image=image)

    async def delete(self, id: int) -> int:
        return await self._image_data.delete(id=id)