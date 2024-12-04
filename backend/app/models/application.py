from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

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