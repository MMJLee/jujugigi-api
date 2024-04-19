# standard lib imports
import re
from typing import Sequence, Optional
from datetime import datetime
from zoneinfo import ZoneInfo

# third party imports
from fastapi import UploadFile

# module imports
from app.exceptions import BaseError
from app.data.image import ImageData
from app.data.user_image import UserImageData
from app.models.image import ImageBase, ImageCreate, ImageUpdate, ImageResponse
from app.models.user_image import UserImageCreate


class ImageLogic:
    def __init__(self, image_data: ImageData, user_image_data: UserImageData):
        self._image_data = image_data
        self._user_image_data = user_image_data

    async def create(self, image_file: UploadFile, user_email: str) -> int:
        image_file.file.seek(0)
        pattern = r"^[1-5]_[a-z0-9_']+[.][a-z]{3,4}$"
        if re.match(pattern, image_file.filename, re.IGNORECASE):
            image = ImageCreate(
                path="images",
                file_name=image_file.filename,
                description=image_file.filename[image_file.filename.find("_") : image_file.filename.rfind(".")].replace("_", " "),
                rarity=image_file.filename[0],
                created_by=user_email,
                updated_by=user_email,
            )
            return await self._image_data.create(image=image, image_file=image_file)
        else:
            raise BaseError({"code": "create:image", "description": "Incorrect file name schema"})

    async def bulk_create(self, image_files: Sequence[UploadFile], user_email: str) -> int:
        existing_images = await self._image_data.read_all()
        count = 0
        for image_file in image_files:
            if image_file.filename in existing_images:
                count += await self.update(image_file=image_file, user_email=user_email)
            else:
                count += await self.create(image_file=image_file, user_email=user_email)
        return count

    async def read(
        self, user_email: Optional[str], user_alias: Optional[str], opened: Optional[bool], limit: int, offset: int
    ) -> Sequence[Optional[ImageResponse]]:
        return await self._image_data.read(user_email=user_email, user_alias=user_alias, opened=opened, limit=limit, offset=offset)

    async def update(self, image_file: UploadFile, user_email: str) -> int:
        image_file.file.seek(0)
        now = datetime.now(tz=ZoneInfo("America/Chicago"))
        pattern = r"^[1-5]_[a-z0-9_']+[.][a-z]{3,4}$"
        if re.match(pattern, image_file.filename, re.IGNORECASE):
            image = ImageUpdate(
                path="images",
                file_name=image_file.filename,
                description=image_file.filename[image_file.filename.find("_") : image_file.filename.rfind(".")].replace("_", " "),
                rarity=image_file.filename[0],
                updated_by=user_email,
                updated_on=now,
            )
            return await self._image_data.update(image=image, image_file=image_file)
        else:
            raise BaseError({"code": "create:image", "description": "Incorrect file name schema"})

    async def delete(self, image_id: int) -> int:
        return await self._image_data.delete(image_id=image_id)

    async def gacha(self, user_email: str) -> Sequence[Optional[ImageResponse]]:
        image_id = await self._image_data.read_random_unowned_image(user_email=user_email)
        user_image = UserImageCreate(user_email=user_email, image_id=image_id, opened=False, created_by=user_email, updated_by=user_email)
        return await self._user_image_data.create(user_image=user_image)

    async def open_image(self, user_email: str) -> Sequence[Optional[ImageResponse]]:
        user_image_id = await self._user_image_data.read_unopened_image(user_email=user_email)
        if user_image_id:
            return await self._image_data.read(user_image_id=user_image_id)
        else:
            return []
