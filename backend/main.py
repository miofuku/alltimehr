from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from app.api import interview
from app.services.resume_analyzer import ResumeAnalyzer

app = FastAPI()

# Config CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create ResumeAnalyzer instance
resume_analyzer = ResumeAnalyzer()

@app.post("/api/applications")
async def submit_application(
    resume: UploadFile = File(...),
    cover_letter: UploadFile = None
):
    """
    Process application materials
    - analyze cv and cover letter
    - if requirements are fulfilled, send out invitation
    - return analysis result
    """
    analysis_result = await resume_analyzer.analyze_and_process(
        resume,
        cover_letter
    )
    
    return analysis_result

# interview route
app.include_router(interview.router, prefix="/api/interview")