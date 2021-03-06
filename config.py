from pydantic import BaseSettings, FilePath, stricturl


class Settings(BaseSettings):
    qna_file_path: FilePath = 'resource/qna.json'
    grade_names_file_path: FilePath = 'resource/grade_names.json'
    cafe_names_file_path: FilePath = 'resource/cafe_names.json'
    db_url: stricturl(tld_required=False, allowed_schemes={'sqlite'})

    class Config:
        env_prefix = 'pilgrim_'
        secrets_dir = '/run/secrets'
