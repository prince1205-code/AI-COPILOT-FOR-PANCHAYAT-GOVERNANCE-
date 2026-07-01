"""
Sahayak AI - Language Service
Singleton factory for LanguageAgent — mirrors voice_service.py pattern.
"""
from functools import lru_cache
from src.agents.language.detector       import LanguageDetector
from src.agents.language.language_agent import LanguageAgent
from src.api.dependencies               import get_memory


@lru_cache(maxsize=1)
def _get_detector() -> LanguageDetector:
    return LanguageDetector()


def get_language_agent() -> LanguageAgent:
    """FastAPI dependency — returns shared LanguageAgent singleton."""
    return LanguageAgent(detector=_get_detector(), memory=get_memory())
