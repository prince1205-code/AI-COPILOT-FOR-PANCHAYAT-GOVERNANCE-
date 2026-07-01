"""
Sahayak AI - Language Agent
Detects language from text and persists it to session memory.
Does NOT translate. Does NOT do TTS.
"""
from src.agents.language.detector import LanguageDetector
from src.services.memory_service  import MemoryService

_SESSION_LANG_KEY = "detected_language"


class LanguageAgent:
    """
    Thin orchestration layer:
        1. Detect language via LanguageDetector
        2. Store result in MemoryService session metadata
        3. Return detection result to caller (Orchestrator / VoiceAgent)
    """

    def __init__(self, detector: LanguageDetector, memory: MemoryService):
        self.detector = detector
        self.memory   = memory

    def detect_and_store(self, text: str, session_id: str) -> dict:
        """
        Detect language of `text` and persist to session.

        Returns
        -------
        dict with keys: detected_language, confidence, method
        """
        result = self.detector.detect(text)

        # Store as a lightweight metadata message so history carries language context
        self.memory.add_message(
            session_id,
            role    = "system",
            content = f"[Language detected: {result['detected_language']}]",
            intent  = "language_detection",
            metadata= {
                _SESSION_LANG_KEY: result["detected_language"],
                "confidence":      result["confidence"],
                "method":          result["method"],
            },
        )

        return result

    def get_session_language(self, session_id: str) -> str | None:
        """Return the most recently detected language for a session, or None."""
        for msg in reversed(self.memory.get_history(session_id)):
            if msg.get("intent") == "language_detection":
                return msg["metadata"].get(_SESSION_LANG_KEY)
        return None
