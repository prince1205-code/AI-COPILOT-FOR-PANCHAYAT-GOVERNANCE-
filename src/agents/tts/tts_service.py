"""
Sahayak AI - TTS Service
Singleton factory for TTSAgent — mirrors voice_service.py pattern.
"""
from functools import lru_cache
from src.agents.tts.speech_generator import SpeechGenerator
from src.agents.tts.audio_service    import AudioService
from src.agents.tts.tts_agent        import TTSAgent


@lru_cache(maxsize=1)
def _get_generator() -> SpeechGenerator:
    return SpeechGenerator()


@lru_cache(maxsize=1)
def _get_audio_service() -> AudioService:
    return AudioService()


def get_tts_agent() -> TTSAgent:
    """FastAPI dependency — returns shared TTSAgent singleton."""
    return TTSAgent(generator=_get_generator(), audio_svc=_get_audio_service())
