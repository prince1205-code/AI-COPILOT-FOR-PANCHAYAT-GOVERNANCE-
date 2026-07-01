"""
Sahayak AI - API Models
Request and Response schemas for all API endpoints.
"""
from typing import Optional
from pydantic import BaseModel, Field


# ----------------------------------------------------------
# /recommend  &  /profile/recommend
# ----------------------------------------------------------

class ProfileRequest(BaseModel):
    age:        Optional[int]   = Field(None, ge=1, le=120, example=28)
    state:      Optional[str]   = Field(None, example="Uttar Pradesh")
    occupation: Optional[str]   = Field(None, example="Farmer")
    income:     Optional[int]   = Field(None, ge=0, example=80000)
    gender:     Optional[str]   = Field(None, example="male")
    top_k:      int             = Field(10, ge=1, le=50)


class SchemeResult(BaseModel):
    scheme_name:  str
    category:     str
    level:        str
    score:        int
    confidence:   str
    reason:       str
    why:          list[str]      # "Why this scheme?" bullets


class RecommendResponse(BaseModel):
    total:   int
    profile: dict
    results: list[SchemeResult]


# ----------------------------------------------------------
# /profile/recommend  (natural language input)
# ----------------------------------------------------------

class NLProfileRequest(BaseModel):
    text:  str = Field(..., example="I am a 28 year old farmer from Gujarat with income 80000")
    top_k: int = Field(10, ge=1, le=50)


class NLProfileResponse(BaseModel):
    extracted_profile: dict
    total:             int
    results:           list[SchemeResult]


# ----------------------------------------------------------
# /chat
# ----------------------------------------------------------

class ChatRequest(BaseModel):
    session_id: str  = Field(..., example="user_abc123")
    message:    str  = Field(..., example="What is PM Kisan?")


class ChatResponse(BaseModel):
    session_id: str
    reply:      str
    intent:     str


# ----------------------------------------------------------
# /scheme
# ----------------------------------------------------------

class SchemeRequest(BaseModel):
    session_id: str = Field(..., example="user_abc123")
    query:      str = Field(..., example="Tell me about Ayushman Bharat")


class ExecutionTraceItem(BaseModel):
    task_id:            str
    name:               str
    label:              str
    agent:              str
    status:             str
    execution_time_ms:  float
    error:              Optional[str] = None


class SchemeResponse(BaseModel):
    session_id:          str
    query:               str
    answer:              str
    intent:              Optional[str] = None
    goal:                Optional[str] = None
    detected_language:   Optional[str] = None
    execution_time_ms:   Optional[float] = None
    execution_trace:     list[ExecutionTraceItem] = Field(default_factory=list)
    tts:                 dict = Field(default_factory=dict)


# ----------------------------------------------------------
# /history/{session_id}
# ----------------------------------------------------------

class MessageRecord(BaseModel):
    role:      str
    content:   str
    intent:    str
    timestamp: str


class HistoryResponse(BaseModel):
    session_id: str
    total:      int
    messages:   list[MessageRecord]


# ----------------------------------------------------------
# /health
# ----------------------------------------------------------

class HealthResponse(BaseModel):
    status:         str
    schemes_loaded: int
    version:        str
