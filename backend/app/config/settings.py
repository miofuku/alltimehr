from pydantic_settings import BaseSettings
from typing import Optional
from google.oauth2.credentials import Credentials
import json
import os

class SMTPSettings(BaseSettings):
    server: str = "smtp.gmail.com"
    port: int = 587
    username: Optional[str] = None
    password: Optional[str] = None
    
    class Config:
        env_prefix = "SMTP_"

class Settings(BaseSettings):
    # OpenAI
    openai_api_key: Optional[str] = None
    
    # SMTP
    smtp: SMTPSettings = SMTPSettings()
    
    # Google Calendar
    google_calendar_creds_file: str = "credentials/credentials.json"
    
    # Security
    secret_key: str = "development_secret_key"
    
    # Server
    base_url: str = "http://localhost:8000"

    @property
    def google_calendar_creds(self) -> Optional[Credentials]:
        """Load Google Calendar credentials from file"""
        try:
            if not os.path.exists(self.google_calendar_creds_file):
                return None
                
            with open(self.google_calendar_creds_file, 'r') as f:
                creds_data = json.load(f)
                
            return Credentials.from_authorized_user_info(creds_data)
        except Exception as e:
            print(f"Error loading Google Calendar credentials: {e}")
            return None
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Create global settings instance
settings = Settings() 