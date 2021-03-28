from pydantic import BaseSettings, DirectoryPath, FilePath


class Settings(BaseSettings):
    qna_file_path: FilePath = 'resource/qna.json'
    grade_names_file_path: FilePath = 'resource/grade_names.json'
    cafe_names_file_path: FilePath = 'resource/cafe_names.json'
    image_path: DirectoryPath = 'resource/images'
    db_url: str = 'sqlite://db.sqlite3'
    dd_on: bool = False

    class Config:
        env_prefix = 'pilgrim_'
        secrets_dir = '/run/secrets'
