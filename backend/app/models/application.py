from pydantic import BaseModel, field_validator
from typing import List, Optional
from datetime import datetime
from app.utils.validation import validate_email_address, validate_phone_number, sanitize_input

class Education(BaseModel):
    """Education history model"""
    school: str
    degree: str
    major: str
    start_date: datetime
    end_date: Optional[datetime]

class Experience(BaseModel):
    """Work experience model"""
    company: str
    position: str
    start_date: datetime
    end_date: Optional[datetime]
    description: str

class Application(BaseModel):
    """Job application model"""
    id: str
    candidate_name: str
    email: str
    phone: str
    education: List[Education]
    experience: List[Experience]
    skills: List[str]
    analysis_score: float
    status: str
    created_at: datetime
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        email = validate_email_address(v)
        if not email:
            raise ValueError('Invalid email address')
        return email
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        if not validate_phone_number(v):
            raise ValueError('Invalid phone number')
        return v
    
    @field_validator('candidate_name')
    @classmethod
    def sanitize_name(cls, v):
        return sanitize_input(v)
  