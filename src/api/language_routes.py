"""
Sahayak AI - Language Detection Routes

POST /api/v1/language/detect  — text → detected_language + confidence
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from src.agents.language.language_agent   import LanguageAgent
from src.agents.language.language_service import get_language_agent

router = APIRouter(prefix="/language", tags=["Language"])


class DetectRequest(BaseModel):
    text:       str = Field(..., example="मुझे पीएम किसान योजना के बारे में बताएं")
    session_id: str = Field(..., example="user_abc123")


class DetectResponse(BaseModel):
    detected_language: str
    confidence:        float
    method:            str   # "script" | "gemini" | "default"
    session_id:        str


@router.post("/detect", response_model=DetectResponse)
def detect_language(
    body:  DetectRequest,
    agent: LanguageAgent = Depends(get_language_agent),
):
    if not body.text.strip():
        raise HTTPException(status_code=422, detail="text must not be empty")

    result = agent.detect_and_store(body.text, body.session_id)
    return DetectResponse(session_id=body.session_id, **result)
