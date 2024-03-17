# standard lib imports
import re
from typing import Sequence, Optional
from datetime import datetime
from zoneinfo import ZoneInfo
# module imports
from exceptions import BaseError
from data.image import ImageData
from logic.payment import PaymentLogic
from models.image import ImageBase, ImageCreate, ImageResponse, ImageUpdate
# third party imports
from fastapi import UploadFile


class ImageLogic:
    def __init__(self, image_data: ImageData, payment_logic: PaymentLogic, gacha_price: int):
        self._image_data = image_data
        self._payment_logic = payment_logic
        self._gacha_price = gacha_price
        
    async def create(self, image_file: UploadFile, user_email: str) -> int:
        pattern = r"^[gj][1-5]_[a-z]+[.][a-z]{3,4}$"
        if re.match(pattern, image_file.filename, re.IGNORECASE):            
            subject_map = {"g": "Geneva", "j": "Juniper"}
            image = ImageCreate(subject=subject_map[image_file.filename[0].lower()], path="images", name=image_file.filename, 
                                mime_type=image_file.content_type, rarity=image_file.filename[1], created_by=user_email, updated_by=user_email)
            return await self._image_data.create(image=image, image_file=image_file)
        else:
            raise Exception({"code": "create:image", "description": "Incorrect file name schema"})        
    
    async def bulk_create(self, image_files: Sequence[UploadFile], user_email: str) -> int:
        count = 0
        for image_file in image_files:
            image_file.file.seek(0)
            count += await self.create(image_file=image_file, user_email=user_email)
        return count
    
    async def read(self, limit: int, offset: int, id: Optional[int], name: Optional[str], user_email: Optional[str]) -> Sequence[Optional[ImageResponse]]:
        return await self._image_data.read(limit=limit, offset=offset, id=id, name=name, user_email=user_email)

    async def update(self, id: int, image: ImageBase, user_email: str) -> int:
        now = datetime.now(tz=ZoneInfo("America/Chicago"))
        image = ImageUpdate(**image.model_dump(), updated_by=user_email, updated_on=now)
        return await self._image_data.update(id=id, image=image)

    async def delete(self, id: int) -> int:
        return await self._image_data.delete(id=id)
        
    async def gacha(self, user_email: str) -> Sequence[Optional[ImageResponse]]:
        id = await self._image_data.unowned_image(user_email=user_email)
        if id:
            try:
                payment_id = await self._payment_logic.process_payment(99)
                if payment_id:
                    return await self._image_data.gacha(user_email=user_email)
            except Exception as e:
                raise BaseError({"code": "gacha", "description": e})
        else:
            raise BaseError({"code": "gacha", "description": "You already own all images"})
