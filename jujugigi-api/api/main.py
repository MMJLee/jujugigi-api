# third party imports
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware

# module imports
from app.config import get_settings
from app.api.events import create_db_connection_pool, close_db_connection_pool
from app.api.handlers import not_found_exception_handler, required_value_handler, auth_exception_handler, token_exception_handler
from app.api.routers import healthcheck, image, user_image, user_alias
from app.exceptions import NotFoundError, RequiredValueError, AuthError, TokenError


def get_application():
    config_settings = get_settings()
    base_url = f"/jujugigi/v{config_settings.API_MAJOR_VERSION}"

    fast_app = FastAPI(
        title=config_settings.API_TITLE,
        version=config_settings.API_VERSION,
        description="API for managing an jujugigi.com",
        docs_url="/jujugigi",
        openapi_url="/jujugigi/openapi.json",
    )

    fast_app.state.config = config_settings

    fast_app.add_middleware(GZipMiddleware, minimum_size=1000)
    fast_app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=config_settings.ALLOW_ORIGIN_REGEX,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # register api event handlers
    fast_app.add_event_handler("startup", create_db_connection_pool(fast_app))
    fast_app.add_event_handler("shutdown", close_db_connection_pool(fast_app))

    # register api exception event handlers
    fast_app.add_exception_handler(NotFoundError, not_found_exception_handler)
    fast_app.add_exception_handler(RequiredValueError, required_value_handler)
    fast_app.add_exception_handler(AuthError, auth_exception_handler)
    fast_app.add_exception_handler(TokenError, token_exception_handler)

    # register api endpoints
    fast_app.include_router(healthcheck.router, prefix=f"{base_url}/healthcheck", tags=["healthcheck"])
    fast_app.include_router(image.router, prefix=f"{base_url}/image", tags=["image"])
    fast_app.include_router(user_image.router, prefix=f"{base_url}/user_image", tags=["user_image"])
    fast_app.include_router(user_alias.router, prefix=f"{base_url}/user_alias", tags=["user_alias"])
    return fast_app


app = get_application()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
