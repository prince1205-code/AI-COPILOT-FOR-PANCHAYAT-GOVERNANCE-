"""
Sahayak AI - Voice API Models
Pydantic schemas for /voice/* endpoints only.
"""
from pydantic import BaseModel, Field


class TranscribeResponse(BaseModel):
    transcript: str


class VoiceProcessResponse(BaseModel):
    session_id:         str
    transcript:         str
    answer:             str
    detected_language:  str   = "English"
    lang_confidence:    float = 0.0


class VoiceErrorResponse(BaseModel):
    error:  str
    detail: str = ""
