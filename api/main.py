from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
import uvicorn

from api.events import (create_db_connection_pool, close_db_connection_pool)
from api.handlers import (not_found_exception_handler, required_value_handler, auth_exception_handler, token_exception_handler)
from exceptions import (NotFoundError, RequiredValueError, AuthError, TokenError)
from config import get_settings
from api.routers import (healthcheck, image, user_image)

def get_application():
    config_settings = get_settings()
    base_url = f'/ecommerce/v{config_settings.API_MAJOR_VERSION}'

    app = FastAPI(
        title=config_settings.API_TITLE,
        version=config_settings.API_VERSION,
        description='API for managing an ecommerce site',
        docs_url='/ecommerce',
        openapi_url='/ecommerce/openapi.json'
    )

    app.state.config = config_settings

    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=config_settings.ALLOW_ORIGIN_REGEX,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(GZipMiddleware, minimum_size=1000)

    # register api event handlers
    app.add_event_handler("startup", create_db_connection_pool(app))
    app.add_event_handler("shutdown", close_db_connection_pool(app))

    # register api exception event handlers
    app.add_exception_handler(NotFoundError, not_found_exception_handler)
    app.add_exception_handler(RequiredValueError, required_value_handler)
    app.add_exception_handler(AuthError, auth_exception_handler)
    app.add_exception_handler(TokenError, token_exception_handler)

    # register api endpoints
    app.include_router(healthcheck.router, prefix=f'{base_url}/healthcheck', tags=['healthcheck'])
    app.include_router(image.router, prefix=f'{base_url}/image', tags=['image'])
    app.include_router(user_image.router, prefix=f'{base_url}/user_image', tags=['user_image'])
    return app

app = get_application()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
