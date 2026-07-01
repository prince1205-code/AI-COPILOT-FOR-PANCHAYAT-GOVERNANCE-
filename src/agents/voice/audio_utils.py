"""
Sahayak AI - Audio Utilities
Validates and normalises raw audio bytes from the browser.
Supported input: webm/opus (MediaRecorder default), wav, ogg, mp3.
"""
import io
from typing import Tuple

# Minimum audio size to be worth transcribing (~0.3 s of webm)
_MIN_BYTES = 1_000
# Maximum accepted payload (10 MB)
_MAX_BYTES = 10 * 1024 * 1024

# MIME type → Gemini inline_data mime_type
_MIME_MAP: dict[str, str] = {
    "audio/webm":       "audio/webm",
    "audio/webm;codecs=opus": "audio/webm",
    "audio/ogg":        "audio/ogg",
    "audio/ogg;codecs=opus": "audio/ogg",
    "audio/wav":        "audio/wav",
    "audio/wave":       "audio/wav",
    "audio/mpeg":       "audio/mpeg",
    "audio/mp3":        "audio/mpeg",
    "audio/mp4":        "audio/mp4",
}


def validate_audio(data: bytes, content_type: str) -> Tuple[bytes, str]:
    """
    Validate audio bytes and return (data, gemini_mime_type).
    Raises ValueError on invalid input.
    """
    if len(data) < _MIN_BYTES:
        raise ValueError("Audio too short — please speak for at least 1 second.")
    if len(data) > _MAX_BYTES:
        raise ValueError("Audio file too large (max 10 MB).")

    # Normalise content_type (strip params like '; codecs=opus')
    ct = content_type.lower().strip()
    gemini_mime = _MIME_MAP.get(ct)

    # Fallback: try base type without params
    if not gemini_mime:
        base = ct.split(";")[0].strip()
        gemini_mime = _MIME_MAP.get(base)

    if not gemini_mime:
        raise ValueError(
            f"Unsupported audio format: '{content_type}'. "
            "Supported: webm, ogg, wav, mp3, mp4."
        )

    return data, gemini_mime


def audio_to_base64(data: bytes) -> str:
    """Return base64-encoded audio string (used by Gemini inline_data)."""
    import base64
    return base64.b64encode(data).decode("utf-8")
