"""
Sahayak AI - Voice Agent
Orchestrates: audio → transcript → language detection → SchemeAgent → answer.
Does NOT duplicate any existing agent logic.
"""
from src.agents.voice.speech_to_text    import SpeechToText
from src.agents.voice.audio_utils       import validate_audio
from src.agents.scheme_agent            import SchemeAgent
from src.services.memory_service        import MemoryService
from src.agents.language.language_agent import LanguageAgent


class VoiceAgent:
    """
    Thin orchestration layer:
        1. Validate + transcribe audio  (SpeechToText)
        2. Pass transcript to SchemeAgent (existing, unchanged)
        3. Persist to MemoryService      (existing, unchanged)
    """

    def __init__(
        self,
        stt:      SpeechToText,
        scheme:   SchemeAgent,
        memory:   MemoryService,
        language: LanguageAgent | None = None,
    ):
        self.stt      = stt
        self.scheme   = scheme
        self.memory   = memory
        self.language = language

    # ----------------------------------------------------------
    # Step 1 — Transcribe only
    # ----------------------------------------------------------

    def transcribe(self, audio_bytes: bytes, content_type: str) -> str:
        """Validate audio and return transcript string."""
        data, mime = validate_audio(audio_bytes, content_type)
        return self.stt.transcribe(data, mime)

    # ----------------------------------------------------------
    # Step 2 — Transcribe + process through SchemeAgent
    # ----------------------------------------------------------

    def process(self, audio_bytes: bytes, content_type: str, session_id: str) -> dict:
        """
        Full pipeline: audio → transcript → language detection → AI answer.

        Returns
        -------
        dict with keys: transcript, answer, session_id, detected_language, lang_confidence
        """
        transcript = self.transcribe(audio_bytes, content_type)

        # Language detection — runs before SchemeAgent so language is in memory
        lang_result = {"detected_language": "English", "confidence": 0.0}
        if self.language:
            lang_result = self.language.detect_and_store(transcript, session_id)

        history = [
            {"role": m["role"], "content": m["content"]}
            for m in self.memory.get_history(session_id)
            if m.get("intent") != "language_detection"   # keep chat history clean
        ]

        self.memory.add_message(session_id, "user", transcript, intent="voice")
        answer = self.scheme.process(transcript, history=history)
        self.memory.add_message(session_id, "assistant", answer, intent="voice")

        return {
            "session_id":        session_id,
            "transcript":        transcript,
            "answer":            answer,
            "detected_language": lang_result["detected_language"],
            "lang_confidence":   lang_result["confidence"],
        }
