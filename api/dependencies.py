# standard lib imports
from typing import Tuple

# third party imports
from databases import Database
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, SecurityScopes
from starlette.requests import Request

# module imports
from exceptions import AuthError
from logic.authorization import AuthorizationLogic
from logic.user import UserLogic
from data.user import UserData
from logic.image import ImageLogic
from data.image import ImageData
from logic.user_image import UserImageLogic
from data.user_image import UserImageData


authorization_logic = AuthorizationLogic()

def get_db(request: Request) -> Database:
    return request.app.state.database

def authorize_user(security_scopes: SecurityScopes, token: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    authorized, username = authorization_logic.authorize_user_for_operation(token=token.credentials, scopes=security_scopes.scopes)
    if not authorized:
        raise AuthError(username=username, scopes=security_scopes.scopes)
    return username

def user_data_dependency(db: Database = Depends(get_db)) -> UserData:
    return UserData(db=db)

def image_data_dependency(db: Database = Depends(get_db)) -> ImageData:
    return ImageData(db=db)

def user_image_data_dependency(db: Database = Depends(get_db)) -> UserImageData:
    return UserImageData(db=db)

def user_logic_dependency(user_data: UserData = Depends(user_data_dependency)) -> UserLogic:
    return UserLogic(user_data=user_data)

def image_logic_dependency(image_data: ImageData = Depends(image_data_dependency)) -> ImageLogic:
    return ImageLogic(image_data=image_data)

def user_image_logic_dependency(user_image_data: UserImageData = Depends(image_data_dependency)) -> UserImageLogic:
    return UserImageLogic(user_image_data=user_image_data)
