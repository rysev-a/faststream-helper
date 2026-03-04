from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_uri: PostgresDsn = Field(default="postgres://user:pass@localhost:5432/db")
