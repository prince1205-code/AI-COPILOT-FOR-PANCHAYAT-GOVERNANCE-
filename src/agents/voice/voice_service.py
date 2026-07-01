"""
Sahayak AI - Voice Service
Singleton factory for VoiceAgent.
Keeps voice dependencies isolated from the main dependency graph.
"""
from functools import lru_cache

from src.agents.voice.speech_to_text       import SpeechToText
from src.agents.voice.voice_agent          import VoiceAgent
from src.agents.scheme_agent               import SchemeAgent
from src.services.memory_service           import MemoryService
from src.agents.language.language_service  import get_language_agent


@lru_cache(maxsize=1)
def _stt() -> SpeechToText:
    return SpeechToText()


@lru_cache(maxsize=1)
def _scheme() -> SchemeAgent:
    return SchemeAgent()


@lru_cache(maxsize=1)
def _memory() -> MemoryService:
    return MemoryService()


def get_voice_agent() -> VoiceAgent:
    """FastAPI dependency — returns shared VoiceAgent instance."""
    return VoiceAgent(
        stt      = _stt(),
        scheme   = _scheme(),
        memory   = _memory(),
        language = get_language_agent(),
    )
