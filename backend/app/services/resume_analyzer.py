from typing import Optional, List
from datetime import datetime, timedelta
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.services.communication_service import CommunicationService
from app.utils.file import extract_text_from_file

class ResumeAnalyzer:
    def __init__(self):
        # Initialize LangChain components
        self.llm = OpenAI(temperature=0)
        
        # Resume analysis prompt
        self.resume_prompt = PromptTemplate(
            input_variables=["resume_text"],
            template="""
            Analyze the following resume and extract key information:
            {resume_text}
            
            Please provide:
            1. Education history (degree, school, dates)
            2. Work experience (company, role, dates, key achievements)
            3. Skills (technical and soft skills)
            4. Overall assessment score (0-1)
            5. Key strengths
            6. Potential areas of concern
            
            Format the response as JSON.
            """
        )
        
        self.resume_chain = LLMChain(
            llm=self.llm,
            prompt=self.resume_prompt
        )
        
        # Skills matching prompt
        self.skills_prompt = PromptTemplate(
            input_variables=["required_skills", "candidate_skills"],
            template="""
            Compare the required skills with candidate's skills:
            Required: {required_skills}
            Candidate: {candidate_skills}
            
            Provide:
            1. Match score (0-1)
            2. Missing critical skills
            3. Additional relevant skills
            4. Recommendation (proceed/reject)
            
            Format as JSON.
            """
        )
        
        self.skills_chain = LLMChain(
            llm=self.llm,
            prompt=self.skills_prompt
        )
        
        self.communication_service = CommunicationService()
        
    async def analyze_and_process(self, resume_file, cover_letter_file: Optional[str] = None):
        analysis = await self.analyze(resume_file, cover_letter_file)
        
        if self._meets_criteria(analysis):
            suggested_times = self._generate_interview_times()
            
            await self.communication_service.send_interview_invitation(
                candidate_email=analysis["email"],
                candidate_name=analysis["name"],
                suggested_times=suggested_times
            )
            
        return analysis
    
    async def analyze(self, resume_file, cover_letter_file: Optional[str] = None):
        # Load and process document
        file_ext = resume_file.filename.lower().split('.')[-1]
        if file_ext == 'pdf':
            loader = PyPDFLoader(resume_file.file)
        else:
            loader = Docx2txtLoader(resume_file.file)
            
        documents = loader.load()
        
        # Split text into manageable chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap=200
        )
        texts = text_splitter.split_documents(documents)
        
        # Analyze resume content
        resume_analysis = await self.resume_chain.arun(
            resume_text="\n".join([t.page_content for t in texts])
        )
        
        # Extract skills and compare with requirements
        skills_analysis = await self.skills_chain.arun(
            required_skills=self.get_required_skills(),
            candidate_skills=resume_analysis["skills"]
        )
        
        # Combine analyses
        analysis = {
            **resume_analysis,
            "skills_match": skills_analysis,
            "overall_score": (
                resume_analysis["score"] * 0.6 +
                skills_analysis["match_score"] * 0.4
            )
        }
        
        if cover_letter_file:
            analysis["cover_letter_score"] = await self._analyze_cover_letter(
                cover_letter_file
            )
            
        return analysis
    
    def get_required_skills(self) -> List[str]:
        """Get required skills for the position"""
        return [
            "Python",
            "React",
            "TypeScript",
            "FastAPI",
            "SQL",
            "Git"
        ]
    
    def _meets_criteria(self, analysis: dict) -> bool:
        """Check if candidate meets requirements"""
        return (
            analysis["overall_score"] >= 0.7 and
            analysis["skills_match"]["recommendation"] == "proceed" and
            not any(
                skill in analysis["skills_match"]["missing_critical_skills"]
                for skill in ["Python", "React"]  # Must-have skills
            )
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