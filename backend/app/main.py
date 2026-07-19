from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import shutil
import os
from .parser import extract_text_from_pdf, extract_contact_info, extract_skills
from .ai_analyzer_simple import SimpleAIResumeAnalyzer
from .interview import InterviewGenerator
from .agentic_system import AgenticResumeSystem

app = FastAPI(title="AI Resume Analyzer - Agentic AI")

# CORS - Allow all origins for testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
analyzer = SimpleAIResumeAnalyzer()
interview = InterviewGenerator()
agentic_system = AgenticResumeSystem()

# Models
class AnalyzeRequest(BaseModel):
    resume_text: str
    job_text: Optional[str] = None

class QuestionRequest(BaseModel):
    role: str = "Machine Learning Engineer"
    question_type: str = "technical"
    count: int = 5
    resume_text: Optional[str] = None

# Basic endpoints
@app.get("/")
async def root():
    return {"message": "AI Resume Analyzer API is running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

# PDF Upload
@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    """Upload and parse a resume PDF"""
    if not file.filename.endswith('.pdf'):
        raise HTTPException(400, "Only PDF files allowed")
    
    os.makedirs("uploads", exist_ok=True)
    file_path = f"uploads/{file.filename}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    text = extract_text_from_pdf(file_path)
    contact = extract_contact_info(text)
    skills = extract_skills(text)
    
    return {
        "filename": file.filename,
        "text_length": len(text),
        "contact": contact,
        "skills": skills,
        "extracted_text": text
    }

# Simple Analysis
@app.post("/analyze-text")
async def analyze_text(request: AnalyzeRequest):
    """Analyze resume text directly"""
    if not request.resume_text:
        raise HTTPException(400, "Resume text is required")
    
    structured = analyzer.extract_structured_info(request.resume_text)
    skills = structured.get("skills", [])
    
    result = {
        "structured_info": structured,
        "skill_count": len(skills),
        "status": "Analysis complete"
    }
    
    if request.job_text:
        job_skills = analyzer._extract_skills(request.job_text)
        resume_skills = set(skills)
        job_skills_set = set(job_skills)
        
        matching = resume_skills.intersection(job_skills_set)
        missing = job_skills_set - resume_skills
        
        match_score = len(matching) / len(job_skills_set) * 100 if job_skills_set else 0
        
        result["match_score"] = match_score
        result["skills_match"] = {
            "matching_skills": list(matching),
            "missing_skills": list(missing),
            "match_percentage": match_score
        }
    
    return result

# Agentic AI Analysis (Core Feature)
@app.post("/agentic-analyze")
async def agentic_analyze(request: AnalyzeRequest):
    """Agentic AI analysis - multi-agent system with ML, Data Science, and AI"""
    if not request.resume_text:
        raise HTTPException(400, "Resume text is required")
    
    result = agentic_system.analyze(request.resume_text, request.job_text)
    return result

# Interview Questions (uses agentic if resume provided)
@app.post("/generate-questions")
async def generate_questions(request: QuestionRequest):
    """Generate interview questions - agentic if resume provided"""
    if request.resume_text:
        # Use agentic system to generate personalized questions
        result = agentic_system.analyze(request.resume_text)
        questions = result.get("questions", [])
        return {"questions": questions}
    
    # Fallback to simple questions
    questions = interview.generate_questions(
        request.role,
        request.question_type,
        request.count
    )
    return {"questions": questions}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)