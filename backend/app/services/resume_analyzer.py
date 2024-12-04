from typing import Optional, List
import spacy
from transformers import pipeline
from datetime import datetime, timedelta
from app.services.communication_service import CommunicationService
from app.utils.file import extract_text_from_file

class ResumeAnalyzer:
    def __init__(self):
        # Load necessary AI models
        self.nlp = spacy.load("en_core_web_lg")
        self.classifier = pipeline("text-classification")
        self.communication_service = CommunicationService()
        
    async def analyze_and_process(self, resume_file, cover_letter_file: Optional[str] = None):
        analysis = await self.analyze(resume_file, cover_letter_file)
        
        if self._meets_criteria(analysis):
            # Generate interview times (next 5 days, 3 slots per day)
            suggested_times = self._generate_interview_times()
            
            # Send interview invitation
            await self.communication_service.send_interview_invitation(
                candidate_email=analysis["email"],
                candidate_name=analysis["name"],
                suggested_times=suggested_times
            )
            
        return analysis
    
    async def analyze(self, resume_file, cover_letter_file: Optional[str] = None):
        # Extract text from resume using file utils
        resume_text = await extract_text_from_file(resume_file)
        if not resume_text:
            raise ValueError("Could not extract text from resume")
        
        # Analyze key information
        analysis = {
            "education": self._analyze_education(resume_text),
            "experience": self._analyze_experience(resume_text),
            "skills": self._analyze_skills(resume_text),
            "score": self._calculate_score(resume_text)
        }
        
        if cover_letter_file:
            cover_letter_text = await extract_text_from_file(cover_letter_file)
            if cover_letter_text:
                analysis["cover_letter_score"] = self._analyze_cover_letter(cover_letter_text)
            
        return analysis
    
    def _analyze_education(self, text):
        # Use NLP to extract education background
        pass
        
    def _analyze_experience(self, text):
        # Analyze work experience
        pass
        
    def _analyze_skills(self, text):
        # Extract skill keywords
        pass
        
    def _calculate_score(self, text):
        # Calculate total score based on analysis
        pass
    
    def _meets_criteria(self, analysis: dict) -> bool:
        """Verify if meets requirements"""
        required_skills = {"python", "react", "typescript"}
        candidate_skills = set(analysis["skills"])
        
        return (
            analysis["score"] >= 0.7 and  # score
            len(required_skills & candidate_skills) >= 2 and  # at least 2 skills
            analysis.get("education_score", 0) >= 0.6  # education requirement
        )
    
    def _generate_interview_times(self) -> List[datetime]:
        """Generate interview times"""
        times = []
        current = datetime.now() + timedelta(days=1)
        
        for _ in range(5):  # next 5 workdays
            if current.weekday() < 5:  # Mon - Fri
                # Morning, midday, afternoon
                times.extend([
                    current.replace(hour=10, minute=0),
                    current.replace(hour=14, minute=0),
                    current.replace(hour=16, minute=0)
                ])
            current += timedelta(days=1)
            
        return times