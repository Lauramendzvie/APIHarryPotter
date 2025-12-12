from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base

class Settings(BaseSettings):
    DB_URL: str = "sqlite+aiosqlite:///./hogwarts.db"
    DBBaseModel = declarative_base()

    class Config:
        case_sensitive = True

settings = Settings()
