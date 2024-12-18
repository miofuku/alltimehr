from typing import Optional, List, Dict, Any, Annotated, Sequence, TypedDict
from datetime import datetime, timedelta
import logging
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolExecutor
from langchain_core.tools import tool
from app.services.communication_service import CommunicationService
from app.config import settings
from app.config.job_requirements import JobRequirements

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('HRAgent')

class AgentState(TypedDict):
    """Type for agent state"""
    messages: Annotated[Sequence[BaseMessage], "Chat message history"]
    resume_text: str
    analysis: Dict[str, Any]
    should_interview: bool

class HRAgent:
    def __init__(self):
        logger.info("Initializing HR Agent")
        self.llm = ChatOpenAI(
            temperature=0,
            openai_api_key=settings.openai_api_key
        )
        self.requirements = JobRequirements.get_all_requirements()
        logger.info(f"Loaded job requirements: {self.requirements}")
        self.communication_service = CommunicationService()
        self.workflow = self._create_workflow()
        logger.info("HR Agent initialized successfully")

    @tool
    def analyze_resume(self, resume_text: str) -> Dict[str, Any]:
        """Analyzes resume content and extracts key information"""
        logger.info("Starting resume analysis")
        prompt = f"""Analyze this resume and extract key information:
        {resume_text[:200]}... # Truncated for logging
        
        Required skills: {self.requirements['technical_skills']}
        Required experience: {self.requirements['experience']}
        Required education: {self.requirements['education']}
        
        Provide:
        1. Education history
        2. Work experience
        3. Skills
        4. Overall assessment
        5. Match score (0-1)
        
        Format as JSON.
        """
        
        logger.debug(f"Sending prompt to LLM: {prompt[:200]}...")
        response = self.llm.invoke(prompt)
        logger.info("Resume analysis completed")
        return response.content

    @tool
    def evaluate_candidate(self, analysis: Dict[str, Any]) -> bool:
        """Evaluates if candidate should be interviewed"""
        logger.info("Starting candidate evaluation")
        prompt = f"""Based on this analysis, should we interview the candidate?
        Analysis: {analysis}
        
        Requirements:
        - Technical skills: {self.requirements['technical_skills']}
        - Experience: {self.requirements['experience']}
        - Education: {self.requirements['education']}
        
        Return true or false.
        """
        
        response = self.llm.invoke(prompt)
        result = response.content.lower().strip() == "true"
        logger.info(f"Evaluation complete. Should interview: {result}")
        return result

    @tool
    async def schedule_interview(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Schedules interview if candidate meets requirements"""
        logger.info("Starting interview scheduling")
        suggested_times = [
            datetime.now() + timedelta(days=i, hours=10)
            for i in range(1, 6)
        ]
        
        logger.info(f"Attempting to send interview invitation to {analysis.get('email', 'unknown')}")
        success = await self.communication_service.send_interview_invitation(
            candidate_email=analysis["email"],
            candidate_name=analysis["name"],
            suggested_times=suggested_times
        )
        
        result = {
            "status": "success" if success else "error",
            "message": "Interview invitation sent" if success else "Failed to send invitation",
            "suggested_times": [t.isoformat() for t in suggested_times]
        }
        logger.info(f"Interview scheduling complete: {result['status']}")
        return result

    def _create_workflow(self) -> StateGraph:
        """Creates the agent workflow graph"""
        # Create tool executor
        tools = [
            self.analyze_resume,
            self.evaluate_candidate,
            self.schedule_interview
        ]

        # Create workflow graph
        workflow = StateGraph(AgentState)

        # Add nodes
        workflow.add_node("analyze", self._analyze_node)
        workflow.add_node("evaluate", self._evaluate_node)
        workflow.add_node("schedule", self._schedule_node)

        # Add edges
        workflow.add_edge("analyze", "evaluate")
        workflow.add_edge("evaluate", "schedule")
        workflow.add_edge("evaluate", END)
        workflow.add_edge("schedule", END)

        # Set entry point
        workflow.set_entry_point("analyze")

        return workflow.compile()

    async def process_application(
        self, 
        resume_file, 
        cover_letter_file: Optional[str] = None
    ) -> Dict[str, Any]:
        """Process a job application"""
        try:
            logger.info(f"Processing application for file: {resume_file.filename}")
            
            # Load and process document
            file_ext = resume_file.filename.lower().split('.')[-1]
            logger.info(f"File extension: {file_ext}")
            
            loader = PyPDFLoader(resume_file.file) if file_ext == 'pdf' else Docx2txtLoader(resume_file.file)
            documents = loader.load()
            logger.info(f"Document loaded successfully, pages: {len(documents)}")
            
            # Split text
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=2000,
                chunk_overlap=200
            )
            texts = text_splitter.split_documents(documents)
            resume_text = "\n".join([t.page_content for t in texts])
            logger.info(f"Text extracted and split into {len(texts)} chunks")

            # Initialize state
            initial_state: AgentState = {
                "messages": [HumanMessage(content=resume_text)],
                "resume_text": resume_text,
                "analysis": {},
                "should_interview": False
            }

            # Run workflow
            logger.info("Starting workflow execution")
            final_state = await self.workflow.arun(initial_state)
            logger.info("Workflow execution completed")

            result = {
                "status": "success",
                "analysis": final_state["analysis"],
                "should_interview": final_state["should_interview"],
                "messages": [msg.content for msg in final_state["messages"]]
            }
            logger.info(f"Application processing complete: {result['status']}")
            return result

        except Exception as e:
            logger.error(f"Error processing application: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "message": f"Failed to process application: {str(e)}"
            }

    async def _analyze_node(self, state: AgentState) -> AgentState:
        """Node for analyzing resume"""
        logger.info("Executing analyze node")
        analysis = await self.analyze_resume(state["resume_text"])
        state["analysis"] = analysis
        state["messages"].append(AIMessage(content=str(analysis)))
        logger.info("Analysis node complete")
        return state

    async def _evaluate_node(self, state: AgentState) -> AgentState:
        """Node for evaluating candidate"""
        logger.info("Executing evaluate node")
        should_interview = await self.evaluate_candidate(state["analysis"])
        state["should_interview"] = should_interview
        state["messages"].append(
            AIMessage(content=f"Should interview: {should_interview}")
        )
        logger.info(f"Evaluation complete: should_interview={should_interview}")
        return state

    async def _schedule_node(self, state: AgentState) -> AgentState:
        """Node for scheduling interview"""
        logger.info("Executing schedule node")
        if state["should_interview"]:
            logger.info("Candidate approved for interview, scheduling...")
            result = await self.schedule_interview(state["analysis"])
            state["messages"].append(AIMessage(content=str(result)))
        else:
            logger.info("Candidate not approved for interview, skipping scheduling")
        return state