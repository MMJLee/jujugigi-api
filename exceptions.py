# standard lib imports
from typing import Optional, Dict, Any, Sequence

class BaseError(Exception):
    def __init__(self, message: Optional[str] = None, tags: Optional[Dict[str, Any]] = None, extras: Optional[Dict[str, Any]] = None) -> None:
        self.message = message
        self.tags = tags or {
            "source": "jujugigi-api",
            "type": type(self).__name__
        }
        self.extras = extras or {}
        super().__init__(message)

class NotFoundError(BaseError):
    def __init__(self, resource_type: str, resource_id: str) -> None:
        message = f"Type {resource_type.title()} with an id value of {resource_id} could not be found."
        extras = {
            "type": resource_type,
            "id": resource_id
        }
        super().__init__(message=message, extras=extras)

class RequiredValueError(BaseError):
    def __init__(self, req_value_list: list) -> None:
        message = f"Required value(s) {req_value_list} missing"
        super().__init__(message=message)

class AuthError(BaseError):
    def __init__(self, error: dict) -> None:
        message = "Unauthorized Operation"
        extras = {
            "username": error.get("username"),
            "scopes": error.get("scopes")
        }
        super().__init__(message=message, extras=extras)

class TokenError(BaseError):
    def __init__(self, error: dict) -> None:
        message = f"{error.get("code")}: {error.get("description")}"
        super().__init__(message=message)
