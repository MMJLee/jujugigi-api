# third party imports
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, SecurityScopes
from starlette.requests import Request
from databases import Database
from supabase import create_client, Client

# module imports
from app.data.stripe import StripeData
from app.exceptions import AuthError
from app.logic.authorization import AuthorizationLogic
from app.logic.stripe import StripeLogic
from app.logic.image import ImageLogic
from app.logic.user_image import UserImageLogic
from app.logic.user_alias import UserAliasLogic
from app.data.image import ImageData
from app.data.user_image import UserImageData
from app.data.user_alias import UserAliasData


authorization_logic = AuthorizationLogic()


def get_db(request: Request) -> Database:
    return request.app.state.database


def get_supabase_client(request: Request) -> Client:
    return create_client(
        request.app.state.config.SUPABASE_URL,
        request.app.state.config.SUPABASE_SERVICE_KEY,
    )


def get_supabase_bucket(request: Request) -> str:
    return request.app.state.config.SUPABASE_BUCKET


def get_supabase_url_timeout(request: Request) -> int:
    return request.app.state.config.SUPABASE_URL_TIMEOUT


def get_stripe_secret_key(request: Request) -> str:
    return request.app.state.config.STRIPE_SECRET_KEY


def get_stripe_product_map(request: Request) -> dict[str, str]:
    return {
        "Geneva": request.app.state.config.STRIPE_GENEVA_PRICE_ID,
        "Juniper": request.app.state.config.STRIPE_JUNIPER_PRICE_ID,
    }


def get_stripe_webhook_secret(request: Request) -> str:
    return request.app.state.config.STRIPE_WEBHOOK_SECRET


def get_domain(request: Request) -> str:
    return request.app.state.config.CLIENT_DOMAIN


def authorize_user(
    security_scopes: SecurityScopes,
    token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
):
    authorized, username = authorization_logic.authorize_user_for_operation(token=token.credentials, scopes=security_scopes.scopes)
    if not authorized:
        raise AuthError({"username": username, "scopes": security_scopes.scopes})
    return username


def image_data_dependency(
    db: Database = Depends(get_db),
    supabase_client: Client = Depends(get_supabase_client),
    supabase_bucket: str = Depends(get_supabase_bucket),
    supabase_url_timeout: int = Depends(get_supabase_url_timeout),
) -> ImageData:
    return ImageData(
        db=db,
        supabase_client=supabase_client,
        supabase_bucket=supabase_bucket,
        supabase_url_timeout=supabase_url_timeout,
    )


def user_image_data_dependency(db: Database = Depends(get_db)) -> UserImageData:
    return UserImageData(db=db)


def user_alias_data_dependency(db: Database = Depends(get_db)) -> UserAliasData:
    return UserAliasData(db=db)


def stripe_data_dependency(db: Database = Depends(get_db)) -> StripeData:
    return StripeData(db=db)


def image_logic_dependency(
    image_data: ImageData = Depends(image_data_dependency),
    user_image_data: UserImageData = Depends(user_image_data_dependency),
) -> ImageLogic:
    return ImageLogic(image_data=image_data, user_image_data=user_image_data)


def user_image_logic_dependency(
    user_image_data: UserImageData = Depends(user_image_data_dependency),
) -> UserImageLogic:
    return UserImageLogic(user_image_data=user_image_data)


def user_alias_logic_dependency(
    user_alias_data: UserAliasData = Depends(user_alias_data_dependency),
) -> UserAliasLogic:
    return UserAliasLogic(user_alias_data=user_alias_data)


def stripe_logic_dependency(
    stripe_data: StripeData = Depends(stripe_data_dependency),
    stripe_secret_key: str = Depends(get_stripe_secret_key),
    stripe_product_map: dict[str, str] = Depends(get_stripe_product_map),
    stripe_webhook_secret: str = Depends(get_stripe_webhook_secret),
    domain_url: str = Depends(get_domain),
    image_logic: ImageLogic = Depends(image_logic_dependency),
) -> StripeLogic:
    return StripeLogic(
        stripe_data=stripe_data,
        stripe_secret_key=stripe_secret_key,
        stripe_product_map=stripe_product_map,
        stripe_webhook_secret=stripe_webhook_secret,
        domain_url=domain_url,
        image_logic=image_logic,
    )
