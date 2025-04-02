from pprint import pprint
from pydantic import BaseModel, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL, create_engine, inspect
from sqlalchemy.orm import Session


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


settings = Settings()

postgres_url = URL.create(
    drivername="postgresql+psycopg",
    username=settings.postgres.user,
    password=settings.postgres.password.get_secret_value(),
    host=settings.postgres.host,
    port=settings.postgres.port,
    database=settings.postgres.dbname,
)

engine = create_engine(postgres_url)

with Session(engine) as s:
    inspector = inspect(engine)
    pprint(inspector.get_table_names("yh"))
