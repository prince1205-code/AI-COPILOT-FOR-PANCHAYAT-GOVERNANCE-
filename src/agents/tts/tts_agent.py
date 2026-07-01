"""
Sahayak AI - TTS Agent
Orchestration layer: cache-check → generate → cache → return MP3 bytes.
Respects per-session stop tokens from AudioService.
Does NOT translate. Does NOT modify existing agents.
"""
import logging
from starlette.concurrency import run_in_threadpool

from src.agents.tts.speech_generator import SpeechGenerator
from src.agents.tts.audio_service    import AudioService

log = logging.getLogger(__name__)


class TTSAgent:
    """
    Thin orchestration:
        1. Check AudioService cache
        2. Register session stop-token
        3. Generate via SpeechGenerator (if not cached)
        4. Store in cache
        5. Return MP3 bytes
    """

    def __init__(self, generator: SpeechGenerator, audio_svc: AudioService):
        self.generator = generator
        self.audio_svc = audio_svc

    def speak(self, text: str, language: str, session_id: str) -> bytes:
        """
        Generate (or retrieve cached) MP3 for `text` in `language`.

        Parameters
        ----------
        text       : AI response text
        language   : detected language (e.g. "Hindi", "Tamil")
        session_id : used for stop-token registration

        Returns
        -------
        bytes — MP3 audio data

        Raises
        ------
        RuntimeError if stop was requested before generation completed
        ValueError   if text is empty after cleaning
        """
        key = self.audio_svc.cache_key(text, language)

        # Cache hit — no generation needed
        cached = self.audio_svc.get(key)
        if cached:
            return cached

        # Register stop-token for this session
        stop_event = self.audio_svc.register_session(session_id)

        try:
            if stop_event.is_set():
                raise RuntimeError("TTS cancelled before generation started.")

            log.info("TTS generating: session=%s lang=%s chars=%d", session_id, language, len(text))
            audio = self.generator.generate(text, language, should_stop=stop_event.is_set)

            # Check stop again after (potentially slow) generation
            if stop_event.is_set():
                raise RuntimeError("TTS cancelled during generation.")

            self.audio_svc.put(key, audio)
            return audio

        finally:
            self.audio_svc.clear_session(session_id)

    def stop(self, session_id: str) -> bool:
        """Signal stop for an in-flight generation. Returns True if session existed."""
        return self.audio_svc.stop_session(session_id)

    async def speak_async(self, text: str, language: str, session_id: str) -> bytes:
        """Run blocking TTS generation in FastAPI's threadpool."""
        return await run_in_threadpool(self.speak, text, language, session_id)
