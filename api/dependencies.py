# module imports
from exceptions import AuthError
from logic.authorization import AuthorizationLogic
from data.image import ImageData
from data.user_image import UserImageData
from logic.payment import PaymentLogic
from logic.image import ImageLogic
from logic.user_image import UserImageLogic
# third party imports
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, SecurityScopes
from starlette.requests import Request
from databases import Database
from supabase import create_client, Client


authorization_logic = AuthorizationLogic()

def get_db(request: Request) -> Database:
    return request.app.state.database

def get_supabase_client(request: Request) -> Client:
    return create_client(request.app.state.config.SUPABASE_URL, request.app.state.config.SUPABASE_SERVICE_KEY)

def get_supabase_bucket(request: Request) -> str:
    return request.app.state.config.SUPABASE_BUCKET

def get_supabase_url_timeout(request: Request) -> int:
    return request.app.state.config.SUPABASE_URL_TIMEOUT

def get_stripe_secret_key(request: Request) -> str:
    return request.app.state.config.STRIPE_SECRET_KEY

def get_gacha_price(request: Request) -> int:
    return request.app.state.config.GACHA_PRICE

def authorize_user(security_scopes: SecurityScopes, token: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    authorized, username = authorization_logic.authorize_user_for_operation(token=token.credentials, scopes=security_scopes.scopes)
    if not authorized:
        raise AuthError(username=username, scopes=security_scopes.scopes)
    return username

def image_data_dependency(db: Database = Depends(get_db), supabase_client: Client = Depends(get_supabase_client), 
                          supabase_bucket: str = Depends(get_supabase_bucket), supabase_url_timeout: int = Depends(get_supabase_url_timeout)) -> ImageData:
    return ImageData(db=db, supabase_client=supabase_client, supabase_bucket=supabase_bucket, supabase_url_timeout=supabase_url_timeout)

def user_image_data_dependency(db: Database = Depends(get_db)) -> UserImageData:
    return UserImageData(db=db)

def payment_logic_dependency(stripe_secret_key: str = Depends(get_stripe_secret_key)) -> PaymentLogic:
    return PaymentLogic(stripe_secret_key=stripe_secret_key)

def image_logic_dependency(image_data: ImageData = Depends(image_data_dependency), payment_logic: PaymentLogic = Depends(payment_logic_dependency),
                           gacha_price: int = Depends(get_gacha_price)) -> ImageLogic:
    return ImageLogic(image_data=image_data, payment_logic=payment_logic, gacha_price=gacha_price)

def user_image_logic_dependency(user_image_data: UserImageData = Depends(user_image_data_dependency)) -> UserImageLogic:
    return UserImageLogic(user_image_data=user_image_data)
