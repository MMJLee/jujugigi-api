# standard lib imports
import os
from enum import Enum

# third party imports
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Environment(str, Enum):
    PRODUCTION = "prod"
    DEVELOPMENT = "dev"
    LOCAL = "local"
    LOCAL_DOCKER = "local_docker"


class Settings(BaseSettings):
    # API config settings
    API_VERSION: str = "1.0.0"
    API_MAJOR_VERSION: str = API_VERSION.split(".", maxsplit=1)[0]
    API_TITLE: str = f"jujugigi-api-v{API_MAJOR_VERSION}"

    # DB connection pool settings
    MIN_DB_POOL_SIZE: int = 1
    MAX_DB_POOL_SIZE: int = 1

    # CORS config settings
    ALLOW_ORIGIN_REGEX: str = r".*"

    # Gacha Price in cents
    GACHA_PRICE: int = os.environ.get("GACHA_PRICE")

    # Auth0 (email and tenant added on token through Auth0 Actions)
    AUTH0_ALLOWED_ISSUERS: str = os.environ.get("AUTH0_ALLOWED_ISSUERS")
    AUTH0_ALGORITHMS: str = os.environ.get("AUTH0_ALGORITHMS")
    AUTH0_DOMAIN: str = os.environ.get("AUTH0_DOMAIN")
    AUTH0_API_AUDIENCE: str = os.environ.get("AUTH0_API_AUDIENCE")
    AUTH0_TOKEN_NAMESPACE: str = os.environ.get("AUTH0_TOKEN_NAMESPACE")
    AUTH0_ISSUER: str = os.environ.get("AUTH0_ISSUER")
    AUTH0_TENANT: str = os.environ.get("AUTH0_TENANT")

    # Supabase storage
    SUPABASE_URL: str = os.environ.get("SUPABASE_URL")
    SUPABASE_BUCKET: str = os.environ.get("SUPABASE_BUCKET")
    SUPABASE_SERVICE_KEY: str = os.environ.get("SUPABASE_SERVICE_KEY")
    SUPABASE_URL_TIMEOUT: int = os.environ.get("SUPABASE_URL_TIMEOUT")

    # Stripe - DEV
    STRIPE_SECRET_KEY: str = os.environ.get("DEV_STRIPE_SECRET_KEY")
    STRIPE_SUCCESS_URL: str = os.environ.get("DEV_STRIPE_SUCCESS_URL")
    STRIPE_CANCEL_URL: str = os.environ.get("DEV_STRIPE_CANCEL_URL")
    STRIPE_GENEVA_PRICE_ID: str = os.environ.get("DEV_STRIPE_GENEVA_PRICE_ID")
    STRIPE_JUNIPER_PRICE_ID: str = os.environ.get("DEV_STRIPE_JUNIPER_PRICE_ID")


class LocalConfig(Settings):
    DATABASE_URL: str = os.environ.get("LOCAL_DATABASE_URL")


class LocalDockerConfig(Settings):
    DATABASE_URL: str = os.environ.get("LOCAL_DOCKER_DATABASE_URL")


env = (os.environ.get("API_ENV") or "local").lower()

if env == "prod":

    class ProductionConfig(Settings):
        ALLOW_ORIGIN_REGEX: str = r"^(https?:\/\/(?:.+\.)?jujugigi\.com(?::\d{1,5})?)$"
        DATABASE_URL: str = os.environ.get("PROD_DATABASE_URL")
        MAX_DB_POOL_SIZE: int = 10

        # Stripe - PROD
        STRIPE_SECRET_KEY: str = os.environ.get("PROD_STRIPE_SECRET_KEY")
        STRIPE_SUCCESS_URL: str = os.environ.get("PROD_STRIPE_SUCCESS_URL")
        STRIPE_CANCEL_URL: str = os.environ.get("PROD_STRIPE_CANCEL_URL")
        STRIPE_GENEVA_PRICE_ID: str = os.environ.get("PROD_STRIPE_GENEVA_PRICE_ID")
        STRIPE_JUNIPER_PRICE_ID: str = os.environ.get("PROD_STRIPE_JUNIPER_PRICE_ID")


def get_settings():
    if env == Environment.PRODUCTION:
        return ProductionConfig()
    elif env == Environment.LOCAL_DOCKER:
        return LocalDockerConfig()
    elif env == Environment.LOCAL:
        return LocalConfig()
    return None
