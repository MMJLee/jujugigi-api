# standard lib imports
import json
from enum import Enum
from typing import Tuple, Sequence
from urllib.request import urlopen

# third party imports
from jose import jwt

# module imports
from app.exceptions import TokenError
from app.config import get_settings


config_settings = get_settings()


class CRUDOperation(str, Enum):
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"


class ResourceType(str, Enum):
    IMAGE = "image"
    USER_IMAGE = "user_image"
    TRANSACTION = "transaction"
    USER_ALIAS = "user_alias"


class AuthorizationLogic:
    def get_value_from_token(self, token: str, key: str, namespace: str = None):
        claims = jwt.get_unverified_claims(token=token)
        if namespace:
            key = f"{namespace}/{key}"
        claim = claims.get(key)
        return claim

    def validate_token(self, token: str, tenant_url: str) -> bool:
        jsonurl = urlopen(f"{tenant_url}.well-known/jwks.json")
        jwks = json.loads(jsonurl.read())
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}

        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"],
                }
        if rsa_key:
            try:
                jwt.decode(
                    token,
                    rsa_key,
                    algorithms=config_settings.AUTH0_ALGORITHMS,
                    audience=config_settings.AUTH0_API_AUDIENCE,
                    issuer=f"{tenant_url}",
                )
                return True
            except jwt.JWTError as e:
                raise TokenError({"code": "jwt_error", "description": f"{e.args}"}) from e
            except Exception:
                raise TokenError({"code": "invalid_header", "description": "Unable to parse authentication token."}) from e
        raise TokenError({"code": "invalid_header", "description": "Unable to find appropriate key"})

    def validate_scopes(self, required_scopes: Sequence[str], token: str) -> bool:
        unverified_claims = jwt.get_unverified_claims(token)
        if unverified_claims.get("scope"):
            token_scopes = unverified_claims["scope"].split()
            if unverified_claims.get("permissions"):
                permissions = unverified_claims.get("permissions") or []
                if len(permissions) > 0:
                    token_scopes = [*token_scopes, *permissions]
            for scope in required_scopes:
                if scope not in token_scopes:
                    return False
            return True
        raise TokenError({"code": "invalid_claims", "description": "Missing scope claim"})

    def authorize_user_for_operation(self, token: str, scopes: Sequence) -> Tuple[bool, str, str]:
        # Retrieve and verify issuer claim on access token
        issuer = self.get_value_from_token(token=token, key="iss")
        if issuer != config_settings.AUTH0_ALLOWED_ISSUERS:
            raise TokenError({"code": "invalid_claims", "description": "Invalid issuer claim"})
        # Validate token using verified issuer as Auth0 tenant
        self.validate_token(token=token, tenant_url=issuer)
        username = self.get_value_from_token(token=token, key="email", namespace=config_settings.AUTH0_TOKEN_NAMESPACE)

        if username is None:
            raise TokenError({"code": "invalid_claims", "description": "No username found on token"})

        tenant = self.get_value_from_token(token=token, key="tenant", namespace=config_settings.AUTH0_TOKEN_NAMESPACE)
        if tenant is None:
            raise TokenError({"code": "invalid_claims", "description": "No tenant found on token"})

        if tenant != config_settings.AUTH0_TENANT:
            raise TokenError({"code": "invalid_claims", "description": "Invalid tenant found on token"})

        valid_scopes = self.validate_scopes(required_scopes=scopes, token=token)
        return valid_scopes, username
