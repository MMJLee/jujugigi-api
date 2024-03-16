# third party imports
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette import status

# module imports
from exceptions import (
    NotFoundError,
    RequiredValueError,
    AuthError,
    TokenError
)

def not_found_exception_handler(request: Request, exc: NotFoundError) -> JSONResponse:
    content = jsonable_encoder(vars(exc))
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=content
    )

def required_value_handler(request: Request, exc: RequiredValueError) -> JSONResponse:
    content = jsonable_encoder(vars(exc))
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=content
    )

def auth_exception_handler(request: Request, exc: AuthError) -> JSONResponse:
    content = jsonable_encoder(vars(exc))
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content=content
    )

def token_exception_handler(request: Request, exc: TokenError) -> JSONResponse:
    content = jsonable_encoder(vars(exc))
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=content
    )