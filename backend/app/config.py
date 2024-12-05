from pydantic_settings import BaseSettings
from typing import Optional

class SMTPSettings(BaseSettings):
    server: str
    port: int
    username: str
    password: str
    
    class Config:
        env_prefix = "SMTP_"

class Settings(BaseSettings):
    smtp: SMTPSettings
    google_calendar_creds_file: str
    min_score_threshold: float = 0.7
    secret_key: str
    openai_api_key: str
    
    class Config:
        env_file = ".env" 