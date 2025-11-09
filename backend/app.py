"""
FastAPI backend for AI Resume Screener.
Provides endpoints for resume upload, parsing, and matching.
"""

import os
import shutil
from typing import Optional
from contextlib import asynccontextmanager
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from models_cache import preload_models
from resume_parser import parse_resume
from matching import perform_matching, llm_enhanced_matching

# Lifespan context manager for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize models on startup and cleanup on shutdown."""
    print("=" * 50)
    print("Starting AI Resume Screener Backend...")
    print("=" * 50)
    preload_models()
    print("=" * 50)
    print("Server ready! Listening on http://localhost:8000")
    print("=" * 50)
    yield
    # Cleanup code here (if needed)
    print("Shutting down...")

# Initialize FastAPI app with lifespan
app = FastAPI(
    title="AI Resume Screener API",
    description="Backend API for resume parsing and job matching",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS for frontend access
# Allow multiple ports for development (Vite may use 5173, 5174, 5175, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174", 
        "http://localhost:5175",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:5175"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory if it doesn't exist
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
async def root():
    """Root endpoint - API health check."""
    return {
        "message": "AI Resume Screener API",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "match": "/match (POST)",
            "match_with_llm": "/match-llm (POST)"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "models_loaded": True
    }

@app.post("/match")
async def match_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    """
    Match resume against job description.
    
    Args:
        resume: Uploaded resume file (PDF, DOCX, or TXT)
        job_description: Job description text
        
    Returns:
        Matching scores, matched skills, missing skills, and suggestions
    """
    print(f"\n{'='*50}")
    print(f"New matching request received")
    print(f"Resume: {resume.filename}")
    print(f"JD length: {len(job_description)} characters")
    print(f"{'='*50}\n")
    
    # Validate file
    if not resume.filename:
        raise HTTPException(status_code=400, detail="No resume file provided")
    
    # Check file extension
    allowed_extensions = ['.pdf', '.docx', '.doc', '.txt']
    file_ext = os.path.splitext(resume.filename)[1].lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format. Allowed: {', '.join(allowed_extensions)}"
        )
    
    # Save uploaded file
    file_path = os.path.join(UPLOAD_DIR, resume.filename)
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(resume.file, buffer)
        print(f"File saved: {file_path}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    
    # Parse resume
    try:
        resume_text = parse_resume(file_path)
        if not resume_text:
            raise HTTPException(status_code=400, detail="Failed to extract text from resume")
    except Exception as e:
        # Clean up file
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Failed to parse resume: {str(e)}")
    
    # Validate JD
    if not job_description or len(job_description) < 50:
        # Clean up file
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(
            status_code=400,
            detail="Job description is too short. Please provide at least 50 characters."
        )
    
    # Perform matching
    try:
        results = perform_matching(resume_text, job_description)
        
        # Clean up uploaded file
        if os.path.exists(file_path):
            os.remove(file_path)
        
        print(f"\nMatching completed successfully!")
        print(f"Overall Score: {results['overall_score']}%")
        print(f"{'='*50}\n")
        
        return JSONResponse(content=results)
    
    except Exception as e:
        # Clean up file
        if os.path.exists(file_path):
            os.remove(file_path)
        print(f"Error during matching: {e}")
        raise HTTPException(status_code=500, detail=f"Matching failed: {str(e)}")

@app.post("/match-llm")
async def match_resume_with_llm(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
    provider: str = Form("openrouter")
):
    """
    Match resume with LLM-enhanced analysis.
    
    Args:
        resume: Uploaded resume file
        job_description: Job description text
        provider: LLM provider ("openrouter" or "gemini")
        
    Returns:
        Standard matching results plus LLM insights
    """
    print(f"\n{'='*50}")
    print(f"LLM-enhanced matching request received")
    print(f"Provider: {provider}")
    print(f"{'='*50}\n")
    
    # Validate file
    if not resume.filename:
        raise HTTPException(status_code=400, detail="No resume file provided")
    
    # Check file extension
    allowed_extensions = ['.pdf', '.docx', '.doc', '.txt']
    file_ext = os.path.splitext(resume.filename)[1].lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format. Allowed: {', '.join(allowed_extensions)}"
        )
    
    # Save uploaded file ONCE
    file_path = os.path.join(UPLOAD_DIR, resume.filename)
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(resume.file, buffer)
        print(f"File saved: {file_path}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    
    # Parse resume once
    try:
        resume_text = parse_resume(file_path)
        if not resume_text:
            raise HTTPException(status_code=400, detail="Failed to extract text from resume")
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Failed to parse resume: {str(e)}")
    
    # Validate JD
    if not job_description or len(job_description) < 50:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(
            status_code=400,
            detail="Job description is too short. Please provide at least 50 characters."
        )
    
    # Perform standard matching
    try:
        results = perform_matching(resume_text, job_description)
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        print(f"Error during matching: {e}")
        raise HTTPException(status_code=500, detail=f"Matching failed: {str(e)}")
    
    # Get LLM insights
    try:
        print(f"Getting LLM insights from {provider}...")
        llm_result = await llm_enhanced_matching(resume_text, job_description, provider)
        results["llm_analysis"] = llm_result
        print(f"LLM analysis completed successfully!")
    except Exception as e:
        print(f"LLM analysis failed: {e}")
        import traceback
        traceback.print_exc()
        # Add error info but continue with standard results
        results["llm_analysis"] = {
            "error": f"LLM analysis failed: {str(e)}",
            "provider": provider
        }
    
    # Clean up uploaded file
    if os.path.exists(file_path):
        os.remove(file_path)
    
    print(f"\nLLM-enhanced matching completed!")
    print(f"Overall Score: {results['overall_score']}%")
    print(f"{'='*50}\n")
    
    return JSONResponse(content=results)

if __name__ == "__main__":
    # Run the server
    # Note: reload=False on Windows to avoid multiprocessing issues
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )
