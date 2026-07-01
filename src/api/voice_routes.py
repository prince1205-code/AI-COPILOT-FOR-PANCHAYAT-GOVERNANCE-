"""
Sahayak AI - Voice API Routes

POST /api/v1/voice/transcribe  — audio → transcript
POST /api/v1/voice/process     — audio → transcript + AI answer

Existing /chat and /scheme endpoints are NOT touched.
"""
from fastapi import APIRouter, Depends, File, Form, UploadFile, HTTPException, Request

from src.api.voice_models            import TranscribeResponse, VoiceProcessResponse
from src.agents.voice.voice_agent    import VoiceAgent
from src.agents.voice.voice_service  import get_voice_agent

router = APIRouter(prefix="/voice", tags=["Voice"])


# ----------------------------------------------------------
# POST /voice/transcribe
# Audio file → transcript only (no AI processing)
# ----------------------------------------------------------

@router.post("/transcribe", response_model=TranscribeResponse)
async def transcribe(
    audio:      UploadFile = File(..., description="Audio file from browser MediaRecorder"),
    agent:      VoiceAgent = Depends(get_voice_agent),
):
    data         = await audio.read()
    content_type = audio.content_type or "audio/webm"

    try:
        transcript = agent.transcribe(data, content_type)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {e}")

    return TranscribeResponse(transcript=transcript)


# ----------------------------------------------------------
# POST /voice/process
# Audio file → transcript + AI answer (full pipeline)
# ----------------------------------------------------------

@router.post("/process", response_model=VoiceProcessResponse)
async def process(
    audio:      UploadFile = File(...,  description="Audio file from browser MediaRecorder"),
    session_id: str        = Form(...,  description="Session ID for conversation memory"),
    agent:      VoiceAgent = Depends(get_voice_agent),
):
    data         = await audio.read()
    content_type = audio.content_type or "audio/webm"

    try:
        result = agent.process(data, content_type, session_id)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Voice processing failed: {e}")

    return VoiceProcessResponse(**result)
