from fastapi import FastAPI, HTTPException, Header, Depends, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import os
import sys

# Add current directory to path so we can import app modules
sys.path.append(os.getcwd())

from app.core.classifier import classifier

app = FastAPI(title="Voice Detection API")

# Define Request Model
class VoiceRequest(BaseModel):
    language: str
    audioFormat: str
    audioBase64: str

# Define Response Model
class VoiceResponse(BaseModel):
    status: str
    language: str
    classification: str
    confidenceScore: float
    explanation: str

# Security
API_KEY = "sk_test_123456789" # In production, use environment variable

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return x_api_key

# Custom Exception Handler for strict JSON error format
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"status": "error", "message": exc.detail},
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"status": "error", "message": f"Internal Server Error: {str(exc)}"},
    )

# Supported Languages Configuration
SUPPORTED_LANGUAGES = ["Tamil", "English", "Hindi", "Malayalam", "Telugu"]

@app.post("/api/voice-detection", response_model=VoiceResponse)
async def detect_voice(request: VoiceRequest, api_key: str = Depends(verify_api_key)):
    
    # Validate Language (Strict)
    if request.language not in SUPPORTED_LANGUAGES:
        raise HTTPException(status_code=400, detail=f"Unsupported language: {request.language}. Must be one of {SUPPORTED_LANGUAGES}")

    # Validate Format (Strict)
    if request.audioFormat.lower() != "mp3":
        raise HTTPException(status_code=400, detail="Invalid audio format. Only 'mp3' is supported.")

    try:
        # Run inference
        result = classifier.predict(request.audioBase64)
        
        return VoiceResponse(
            status="success",
            language=request.language,
            classification=result["classification"],
            confidenceScore=result["confidenceScore"],
            explanation=result["explanation"]
        )
        
    except Exception as e:
        # Log the error
        print(f"Error processing request: {e}")
        # Re-raise to be caught by global handler
        raise e

@app.get("/")
def root():
    return {
        "message": "Voice Detection API is running",
        "supported_languages": SUPPORTED_LANGUAGES,
        "version": "1.0.0",
        "method": "Artifact-based Deepfake Detection (Language Agnostic)"
    }
