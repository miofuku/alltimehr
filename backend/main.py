from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from app.api import interview
from app.services.resume_analyzer import HRAgent

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize HR Agent
hr_agent = HRAgent()

@app.post("/api/applications")
async def submit_application(
    resume: UploadFile = File(...),
    cover_letter: UploadFile = None
):
    """
    Process job application using HR Agent
    - Analyzes resume and cover letter
    - Makes hiring decisions
    - Schedules interviews if appropriate
    """
    result = await hr_agent.process_application(resume, cover_letter)
    return result

# Include interview routes
app.include_router(interview.router, prefix="/api/interview")