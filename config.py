from pathlib import Path

from pydantic import BaseSettings, DirectoryPath


class Settings(BaseSettings):
    image_path: Path = 'images'
    resource_path: DirectoryPath = 'resource'
    db_url: str = 'sqlite://db.sqlite3'
    dd_on: bool = False
    question_offset: int = 1

    class Config:
        env_prefix = 'pilgrim_'
        secrets_dir = '/run/secrets'
