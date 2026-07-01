"""
Sahayak AI - TTS API Routes

POST /api/v1/tts/speak  — text + language → MP3 audio stream
POST /api/v1/tts/stop   — cancel in-flight generation for a session

Existing /voice, /language, /chat, /scheme endpoints are NOT touched.
"""
import logging
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.responses import StreamingResponse
import io

from src.api.tts_models          import SpeakRequest, StopRequest, StopResponse
from src.agents.tts.tts_agent    import TTSAgent
from src.agents.tts.tts_service  import get_tts_agent

log    = logging.getLogger(__name__)
router = APIRouter(prefix="/tts", tags=["TTS"])


# ----------------------------------------------------------
# POST /tts/speak
# text + language → streaming MP3
# ----------------------------------------------------------

@router.post("/speak")
async def speak(
    body:  SpeakRequest,
    agent: TTSAgent = Depends(get_tts_agent),
):
    if not body.text.strip():
        raise HTTPException(status_code=422, detail="text must not be empty")

    try:
        audio_bytes = await agent.speak_async(
            text       = body.text,
            language   = body.language,
            session_id = body.session_id,
        )
    except RuntimeError as e:
        log.info("TTS speak cancelled: session=%s", body.session_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        log.exception("TTS speak error: session=%s", body.session_id)
        raise HTTPException(status_code=500, detail=f"TTS generation failed: {e}")

    return StreamingResponse(
        io.BytesIO(audio_bytes),
        media_type="audio/mpeg",
        headers={
            "Content-Length":      str(len(audio_bytes)),
            "Content-Disposition": "inline; filename=response.mp3",
            "Cache-Control":       "private, max-age=300",
            "X-TTS-Language":      body.language,
            "X-TTS-Session":       body.session_id,
        },
    )


# ----------------------------------------------------------
# POST /tts/stop
# Cancel in-flight generation for a session
# ----------------------------------------------------------

@router.post("/stop", response_model=StopResponse)
async def stop(
    body:  StopRequest,
    agent: TTSAgent = Depends(get_tts_agent),
):
    stopped = agent.stop(body.session_id)
    return StopResponse(session_id=body.session_id, stopped=stopped)
