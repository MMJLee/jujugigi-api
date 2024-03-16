# standard lib imports
from enum import Enum
import os
from typing import Sequence
from pydantic_settings import BaseSettings

class Environment(str, Enum):
    PRODUCTION = 'prod'
    DEVELOPMENT = 'dev'
    LOCAL = 'local'
    LOCAL_DOCKER = 'local_docker'
    
class Settings(BaseSettings):
    # API config settings
    API_VERSION: str = '1.0.0' 
    API_MAJOR_VERSION: str = API_VERSION.split('.')[0]
    API_TITLE: str = f'ecommerce-demo-v{API_MAJOR_VERSION}'
    
    # DB connection pool settings
    MIN_DB_POOL_SIZE: int = 1
    MAX_DB_POOL_SIZE: int = 1
    
    # CORS config settings
    ALLOW_ORIGIN_REGEX: str = r'.*'
    
    # Auth0
    ALLOWED_ISSUERS: Sequence[str] = ['https://login.mjmlee.com/','https://mjlee.us.auth0.com/']
    AUTH0_DOMAIN: str = 'mjlee.auth0.com'
    AUTH0_ALGORITHMS: str = "RS256"
    AUTH0_API_AUDIENCE: str = 'https://mjmlee.com'
    AUTH0_TOKEN_NAMESPACE: str = os.environ.get('AUTH0_TOKEN_NAMESPACE') #Auth0 Actions
    AUTH0_ISSUER: str = 'https://mjlee.auth0.com/'

class LocalConfig(Settings):
    engine: str = 'postgres'
    username: str = 'postgres'
    password: str = 'postgres'
    host: str = 'localhost'
    port: str = '5432'
    db_name: str = 'postgres'
    DATABASE_URL: str = f'{engine}://{username}:{password}@{host}:{port}/{db_name}'
    
class LocalDockerConfig(Settings): 
    engine: str = 'postgres'
    username: str = 'postgres'
    password: str = 'postgres'
    host: str = 'host.docker.internal'
    port: str = '5432'
    db_name: str = 'postgres'
    DATABASE_URL: str = f'{engine}://{username}:{password}@{host}:{port}/{db_name}'
    
class DevelopmentConfig(Settings):
    MAX_DB_POOL_SIZE:int = 5
    engine: str = os.environ.get('DEV_PG_ENGINE')
    username: str = os.environ.get('DEV_PG_USER')
    password: str = os.environ.get('DEV_PG_PASS')
    host: str = os.environ.get('DEV_PG_HOST')
    port: str = os.environ.get('DEV_PG_PORT')
    db_name: str = os.environ.get('DEV_PG_DB_NAME')
    DATABASE_URL: str = f'{engine}://{username}:{password}@{host}:{port}/{db_name}'

env = (os.environ.get('API_ENV') or 'local').lower()

if env == 'prod':
    class ProductionConfig(Settings):
        MAX_DB_POOL_SIZE: int = 10
        ALLOW_ORIGIN_REGEX: str = r'^(https?:\/\/(?:.+\.)?mjlee\.dev(?::\d{1,5})?)$'
        engine: str = os.environ.get('PROD_PG_ENGINE')
        username: str = os.environ.get('PROD_PG_USER')
        password: str = os.environ.get('PROD_PG_PASS')
        host: str = os.environ.get('PROD_PG_HOST')
        port: str = os.environ.get('PROD_PG_PORT')
        db_name: str = os.environ.get('PROD_PG_DB_NAME')
        DATABASE_URL: str = f'{engine}://{username}:{password}@{host}:{port}/{db_name}'

def get_settings():   
    if env == Environment.PRODUCTION:
        return ProductionConfig()
    elif env == Environment.DEVELOPMENT:
        return DevelopmentConfig()
    elif env == Environment.LOCAL_DOCKER:
        return LocalDockerConfig()
    elif env == Environment.LOCAL:
        return LocalConfig()
    return None
