# standard lib imports
from typing import Optional, Sequence

# third party imports
from databases import Database

# module imports
from app.models.user_alias import UserAlias, UserAliasCreate, UserAliasUpdate
from app.utils import build_insert_statement, build_update_statement


class UserAliasData:
    def __init__(self, db: Database) -> None:
        self._db = db

    async def create(self, user_alias: UserAliasCreate) -> int:
        mapped_dict = user_alias.model_dump()
        fields_statement, values_statement = build_insert_statement(mapped_dict=mapped_dict)
        return await self._db.fetch_val(
            query=f"""
                WITH create_user_alias AS (
                    INSERT INTO user_alias ({fields_statement})
                    VALUES ({values_statement}) RETURNING *
                ) SELECT COUNT(*) as created 
                FROM create_user_alias;
            """,
            values=mapped_dict,
            column="created",
        )

    async def read(self, user_alias: Optional[str] = None, user_email: Optional[str] = None, limit: int = 10, offset: int = 0) -> Sequence[Optional[UserAlias]]:
        filter_statement = ""
        values = {"limit": limit, "offset": offset}

        if user_alias:
            filter_statement = "WHERE ua.user_alias ILIKE :user_alias"
            values["user_alias"] = user_alias

        if user_email:
            filter_statement = "WHERE ua.user_email = :user_email"
            values["user_email"] = user_email

        records = await self._db.fetch_all(
            query=f"""SELECT * FROM user_alias ua
                {filter_statement}
                LIMIT :limit OFFSET :offset
            """,
            values=values,
        )
        user_alias_response = []
        if records:
            for record in records:
                user_alias_response.append(UserAlias(**dict(record)))
        return user_alias_response

    async def update(self, user_email: str, user_alias: UserAliasUpdate) -> int:
        mapped_dict = user_alias.model_dump(exclude_unset=True)
        mapped_dict["user_email"] = user_email
        update_statement = build_update_statement(mapped_dict=mapped_dict)
        return await self._db.fetch_val(
            query=f"""
                WITH update_user_alias as (
                    UPDATE user_alias SET {update_statement}
                    WHERE user_email = :user_email RETURNING *
                ) SELECT COUNT(*) as updated 
                FROM update_user_alias
            """,
            values=mapped_dict,
            column="updated",
        )

    async def delete(self, user_alias_id: int) -> int:
        return await self._db.fetch_val(
            query="""
                WITH delete_user_alias as (
                    DELETE FROM user_alias 
                    WHERE user_alias_id = :user_alias_id RETURNING *
                ) SELECT count(*) as deleted 
                FROM delete_user_alias;
            """,
            values={"user_alias_id": user_alias_id},
            column="deleted",
        )

    async def daily_dollar(self, user_email: str) -> int:
        return await self._db.fetch_val(
            query="""
                WITH update_user_alias as (
                    UPDATE user_alias SET daily_dollar = current_timestamp
                    WHERE user_email = :user_email RETURNING *
                ) SELECT COUNT(*) as updated 
                FROM update_user_alias
            """,
            values={"user_email": user_email},
            column="updated",
        )
