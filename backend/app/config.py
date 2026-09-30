from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    database_url: str = "sqlite:///./plagiarism.db"
    secret_key: str = "change-this-secret-key"
    access_token_expire_minutes: int = 60
    embedding_model: str = "all-MiniLM-L6-v2"
    semantic_weight: float = 0.60
    lexical_weight: float = 0.20
    ngram_weight: float = 0.20
    max_file_size_mb: int = 10
    upload_dir: str = "uploads"
    report_dir: str = "generated_reports"
    frontend_url: str = "http://localhost:5173"
    algorithm: str = "HS256"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
