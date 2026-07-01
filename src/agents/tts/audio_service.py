"""
Sahayak AI - Audio Service
Single responsibility: cache + session stop-token registry.
  - LRU cache: hash(text+lang) → MP3 bytes  (avoids re-generating identical responses)
  - Stop registry: session_id → Event        (allows /tts/stop to cancel in-flight generation)
"""
import hashlib
import logging
import threading
from collections import OrderedDict

log = logging.getLogger(__name__)

_CACHE_MAX = 128   # max cached audio entries (~128 × ~50 KB ≈ 6 MB ceiling)


class AudioService:
    """Thread-safe LRU cache + stop-token registry. Safe as singleton."""

    def __init__(self, max_size: int = _CACHE_MAX):
        self._cache:    OrderedDict[str, bytes] = OrderedDict()
        self._max       = max_size
        self._lock      = threading.Lock()
        # session_id → threading.Event (set = stop requested)
        self._stop_flags: dict[str, threading.Event] = {}

    # ── Cache ──────────────────────────────────────────────────────────────────

    @staticmethod
    def cache_key(text: str, language: str) -> str:
        return hashlib.sha256(f"{language.lower()}::{text}".encode()).hexdigest()[:32]

    def get(self, key: str) -> bytes | None:
        with self._lock:
            if key in self._cache:
                self._cache.move_to_end(key)
                log.debug("TTS cache HIT  key=%s", key[:8])
                return self._cache[key]
        return None

    def put(self, key: str, audio: bytes) -> None:
        with self._lock:
            if key in self._cache:
                self._cache.move_to_end(key)
            else:
                if len(self._cache) >= self._max:
                    evicted = self._cache.popitem(last=False)
                    log.debug("TTS cache evict key=%s", evicted[0][:8])
                self._cache[key] = audio
            log.debug("TTS cache STORE key=%s size=%d", key[:8], len(audio))

    # ── Stop-token registry ────────────────────────────────────────────────────

    def register_session(self, session_id: str) -> threading.Event:
        """Create (or reset) a stop-event for a session. Returns the event."""
        with self._lock:
            event = threading.Event()
            self._stop_flags[session_id] = event
        return event

    def stop_session(self, session_id: str) -> bool:
        """Signal stop for a session. Returns True if session was active."""
        with self._lock:
            event = self._stop_flags.get(session_id)
        if event:
            event.set()
            log.info("TTS stop signalled session=%s", session_id)
            return True
        return False

    def is_stopped(self, session_id: str) -> bool:
        with self._lock:
            event = self._stop_flags.get(session_id)
        return bool(event and event.is_set())

    def clear_session(self, session_id: str) -> None:
        with self._lock:
            self._stop_flags.pop(session_id, None)
