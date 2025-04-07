from contextlib import contextmanager
from typing import Iterable

from psycopg import sql, Cursor
from psycopg.conninfo import make_conninfo
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool
from pydantic import BaseModel, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseModel):
    host: str = Field(default="127.0.0.1")
    port: int = Field(default="5432")
    user: str = Field(default="postgres")
    password: SecretStr = Field(default_factory=lambda: SecretStr(""))
    dbname: str = Field(default="postgres_db")


class Settings(BaseSettings):
    postgres: PostgresSettings
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        env_nested_delimiter="_",
        case_sensitive=False,
    )


class PostgresClient:
    def __init__(self):
        self._config = Settings()
        self._conninfo = make_conninfo(
            host=self._config.postgres.host,
            port=self._config.postgres.port,
            dbname=self._config.postgres.dbname,
            user=self._config.postgres.user,
            password=self._config.postgres.password.get_secret_value(),
        )
        self._pool = ConnectionPool(conninfo=self._conninfo)
        self._pool.open()

    def close(self) -> None:
        self._pool.close()

    def connection(self):
        return self._pool.connection()

    @contextmanager
    def cursor(self, factory_dict_row: bool = True, **kwargs):
        if factory_dict_row:
            kwargs["row_factory"] = dict_row
        with self.connection() as conn:
            with conn.cursor(**kwargs) as cur:
                yield cur

    def build_insert_query(
        self,
        record: BaseModel | dict,
        table: str,
        extra_clauses: list[sql.SQL] | None = None,
    ) -> tuple[sql.SQL, dict]:
        if "." in table:
            tbl = sql.SQL(".").join(map(sql.Identifier, table.split(".", 1)))
        else:
            tbl = sql.Identifier(table)

        params = self._normalize_record(record)

        query_base = sql.SQL("INSERT INTO {tbl} ({col}) VALUES ({val})").format(
            tbl=tbl,
            col=sql.SQL(", ").join(map(sql.Identifier, params.keys())),
            val=sql.SQL(", ").join(map(sql.Placeholder, params.keys())),
        )
        query_full = sql.SQL(" ").join([query_base, *(extra_clauses or [])])

        return query_full, params

    def insert_models(
        self,
        cur: Cursor,
        records: Iterable[BaseModel | dict],
        table: str,
        extra_clauses: list[sql.SQL] | None = None,
    ):
        records = list(records)
        if not records:
            return
        records_dump = [self._normalize_record(r) for r in records]

        query_base, _ = self.build_insert_query(records_dump[0], table)
        query_full = sql.SQL(" ").join([query_base, *(extra_clauses or [])])

        cur.executemany(query_full, records_dump)

    @staticmethod
    def _normalize_record(record: dict | BaseModel) -> dict:
        match record:
            case BaseModel():
                return record.model_dump()
            case dict():
                return record.copy()
            case _:
                raise TypeError(f"Expected BaseModel or dict, got {type(record).__name__}")


# @lru_cache()
def get_pool():
    return PostgresClient()


if __name__ == "__main__":
    client = get_pool()
    with client.cursor() as cur:
        print(cur.connection)
