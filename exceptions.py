# standard lib imports
from typing import Optional, Dict, Any, Sequence

class BaseException(Exception):
    def __init__(self, message: Optional[str] = None, tags: Optional[Dict[str, Any]] = None, extras: Optional[Dict[str, Any]] = None) -> None:
        self.message = message
        self.tags = tags or {
            'source': 'ecommerce api',
            'type': type(self).__name__
        }
        self.extras = extras or {}
        super().__init__(message)

class NotFoundError(BaseException):
    def __init__(self, resource_type: str, resource_id: str) -> None:
        message = f"Type '{resource_type.title()}' with an id value of '{resource_id}' could not be found."
        extras = {
            'type': resource_type,
            'id': resource_id
        }
        super().__init__(message=message, extras=extras)

class RequiredValueError(BaseException):
    def __init__(self, req_value_list: list) -> None:
        message = f"Required value(s) '{req_value_list}' missing"
        super().__init__(message=message)

class AuthError(BaseException):
    def __init__(self, username: str, scopes: Sequence[str]) -> None:
        message = f'Unauthorized Operation for User: {username}, Security Scopes: {scopes}'
        extras = {
            'username': username,
            'scopes': scopes
        }
        super().__init__(message=message, extras=extras)

class TokenError(BaseException):
    def __init__(self, error) -> None:
        message = f"{error.get('code')}: {error.get('description')}"
        super().__init__(message=message)