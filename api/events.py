from typing import Callable
from databases import Database
from fastapi import FastAPI

def create_db_connection_pool(app: FastAPI) -> Callable:
    async def _create_db_connection_pool() -> None:
        config = app.state.config
        app.state.database = Database(
            url=config.DATABASE_URL,
            min_size=config.MIN_DB_POOL_SIZE,
            max_size=config.MAX_DB_POOL_SIZE
        )
        await app.state.database.connect()
    return _create_db_connection_pool

def close_db_connection_pool(app: FastAPI) -> Callable:
    async def _close_db_connection_pool() -> None:
        await app.state.database.disconnect()
    return _close_db_connection_pool