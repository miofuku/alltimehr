from typing import Optional, List
from datetime import datetime, timedelta
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.services.communication_service import CommunicationService
from app.config.job_requirements import JobRequirements

class HRAgent:
    def __init__(self):
        # Initialize LLM
        self.llm = ChatOpenAI(temperature=0)
        
        # Get job requirements
        self.requirements = JobRequirements.get_all_requirements()
        
        # Initialize memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # Define tools
        self.tools = [
            Tool(
                name="analyze_resume",
                func=self._analyze_resume,
                description="Analyzes a resume document and extracts key information"
            ),
            Tool(
                name="evaluate_skills",
                func=self._evaluate_skills,
                description="Evaluates candidate's skills against job requirements"
            ),
            Tool(
                name="schedule_interview",
                func=self._schedule_interview,
                description="Schedules an interview if candidate meets requirements"
            )
        ]
        
        # Initialize agent
        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            memory=self.memory,
            verbose=True
        )
        
        self.communication_service = CommunicationService()

    async def process_application(self, resume_file, cover_letter_file: Optional[str] = None):
        """Process a job application"""
        try:
            # Load document
            file_ext = resume_file.filename.lower().split('.')[-1]
            loader = PyPDFLoader(resume_file.file) if file_ext == 'pdf' else Docx2txtLoader(resume_file.file)
            documents = loader.load()
            
            # Split text
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=2000,
                chunk_overlap=200
            )
            texts = text_splitter.split_documents(documents)
            resume_text = "\n".join([t.page_content for t in texts])
            
            # Let agent analyze and make decisions
            result = await self.agent.arun(
                f"""Process this job application:
                Resume: {resume_text}
                Cover Letter: {cover_letter_file if cover_letter_file else 'Not provided'}
                
                Follow these steps:
                1. Analyze the resume
                2. Evaluate skills against requirements
                3. If candidate meets requirements, schedule an interview
                4. Provide a detailed assessment report
                """
            )
            
            return result
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to process application: {str(e)}"
            }

    def _analyze_resume(self, text: str) -> dict:
        """Tool: Resume Analysis"""
        try:
            analysis = self.llm.predict(
                f"""Analyze this resume and extract key information:
                {text}
                
                Provide:
                1. Education history
                2. Work experience
                3. Skills
                4. Overall assessment
                
                Format as JSON.
                """
            )
            return analysis
        except Exception as e:
            return {"error": f"Resume analysis failed: {str(e)}"}

    def _evaluate_skills(self, skills: List[str]) -> dict:
        """Tool: Skills Evaluation"""
        try:
            evaluation = self.llm.predict(
                f"""Evaluate these skills against our requirements:
                Candidate skills: {skills}
                Required skills: {self.requirements['technical_skills']['must_have']}
                Preferred skills: {self.requirements['technical_skills']['preferred']}
                Required experience: {self.requirements['experience']}
                
                Provide:
                1. Skills match score (0-1)
                2. Missing critical (must-have) skills
                3. Missing preferred skills
                4. Experience assessment
                5. Recommendation (proceed/reject)
                
                Format as JSON.
                """
            )
            return evaluation
        except Exception as e:
            return {"error": f"Skills evaluation failed: {str(e)}"}

    async def _schedule_interview(self, candidate_info: dict) -> dict:
        """Tool: Interview Scheduling"""
        try:
            # Generate interview slots
            suggested_times = [
                datetime.now() + timedelta(days=i, hours=10)
                for i in range(1, 6)
            ]
            
            # Send invitation
            success = await self.communication_service.send_interview_invitation(
                candidate_email=candidate_info["email"],
                candidate_name=candidate_info["name"],
                suggested_times=suggested_times
            )
            
            return {
                "status": "success" if success else "error",
                "message": "Interview invitation sent" if success else "Failed to send invitation",
                "suggested_times": [t.isoformat() for t in suggested_times]
            }
        except Exception as e:
            return {"error": f"Interview scheduling failed: {str(e)}"}