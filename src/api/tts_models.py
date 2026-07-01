"""
Sahayak AI - TTS API Models
Pydantic schemas for /tts/* endpoints only.
"""
from pydantic import BaseModel, Field


class SpeakRequest(BaseModel):
    text:       str = Field(...,          example="PM Kisan Yojana provides ₹6000 per year.")
    language:   str = Field("Hindi",      example="Hindi")
    session_id: str = Field(...,          example="user_abc123")


class StopRequest(BaseModel):
    session_id: str = Field(..., example="user_abc123")


class StopResponse(BaseModel):
    session_id: str
    stopped:    bool
