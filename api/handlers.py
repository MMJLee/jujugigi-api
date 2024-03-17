# module imports
from exceptions import (NotFoundError, RequiredValueError, AuthError, TokenError)
# third party imports
from fastapi import Request, encoders, responses
from starlette import status

def not_found_exception_handler(request: Request, exc: NotFoundError) -> responses.JSONResponse:
    content = encoders.jsonable_encoder(vars(exc))
    return responses.JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=content
    )

def required_value_handler(request: Request, exc: RequiredValueError) -> responses.JSONResponse:
    content = encoders.jsonable_encoder(vars(exc))
    return responses.JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=content
    )

def auth_exception_handler(request: Request, exc: AuthError) -> responses.JSONResponse:
    content = encoders.jsonable_encoder(vars(exc))
    return responses.JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content=content
    )

def token_exception_handler(request: Request, exc: TokenError) -> responses.JSONResponse:
    content = encoders.jsonable_encoder(vars(exc))
    return responses.JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=content
    )