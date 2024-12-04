from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from app.services.resume_analyzer import ResumeAnalyzer
from app.models.application import Application

app = FastAPI()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/applications")
async def submit_application(
    resume: UploadFile = File(...),
    cover_letter: UploadFile = None
):
    # 处理申请材料
    analyzer = ResumeAnalyzer()
    analysis_result = await analyzer.analyze(resume, cover_letter)
    
    return analysis_result 