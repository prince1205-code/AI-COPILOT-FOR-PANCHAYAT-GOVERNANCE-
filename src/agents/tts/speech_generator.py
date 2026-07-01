"""
Sahayak AI - Speech Generator
Single responsibility: text → MP3 bytes via gTTS.
Handles language mapping, markdown stripping, and natural sentence chunking.
"""
import io
import logging
import re
from collections.abc import Callable
from gtts import gTTS

log = logging.getLogger(__name__)

# ── Language → BCP-47 / gTTS lang code ────────────────────────────────────────
_LANG_MAP: dict[str, str] = {
    "english":   "en",
    "hindi":     "hi",
    "bengali":   "bn",
    "marathi":   "mr",
    "gujarati":  "gu",
    "punjabi":   "pa",
    "tamil":     "ta",
    "telugu":    "te",
    "kannada":   "kn",
    "malayalam": "ml",
    "urdu":      "ur",
    # Bhojpuri and Awadhi have no dedicated gTTS code — fall back to Hindi
    "bhojpuri":  "hi",
    "awadhi":    "hi",
}

_DEFAULT_LANG = "hi"   # Hindi as project default
_CHUNK_CHARS  = 450    # gTTS handles shorter natural chunks more reliably

# Markdown / special chars to strip before TTS
_MD_STRIP = re.compile(
    r"```.*?```|`[^`]+`|#{1,6}\s|[*_~>|]|\[([^\]]+)\]\([^)]+\)",
    re.DOTALL,
)


def _clean(text: str) -> str:
    """Strip markdown, collapse whitespace."""
    text = _MD_STRIP.sub(r"\1", text)
    text = re.sub(r"\n{2,}", ". ", text)
    text = re.sub(r"\s+([,.!?;:।])", r"\1", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _split_sentences(text: str) -> list[str]:
    """Split on sentence boundaries, respecting chunk size limit."""
    # Split on common sentence boundaries while preserving punctuation for pauses.
    raw = re.split(r"(?<=[.!?।])\s+", text)
    chunks: list[str] = []
    current = ""
    for sentence in raw:
        if len(current) + len(sentence) + 1 <= _CHUNK_CHARS:
            current = (current + " " + sentence).strip()
        else:
            if current:
                chunks.append(current)
            # If a single sentence exceeds limit, split on softer pause marks.
            if len(sentence) > _CHUNK_CHARS:
                parts = re.split(r"(?<=[,;:])\s+", sentence)
                sub = ""
                for p in parts:
                    if len(sub) + len(p) + 1 <= _CHUNK_CHARS:
                        sub = (sub + " " + p).strip()
                    else:
                        if sub:
                            chunks.append(sub)
                        sub = p
                if sub:
                    chunks.append(sub)
                current = ""
            else:
                current = sentence
    if current:
        chunks.append(current)
    return [c for c in chunks if c.strip()]


def _gtts_lang(language: str) -> str:
    return _LANG_MAP.get(language.strip().lower(), _DEFAULT_LANG)


class SpeechGenerator:
    """
    Stateless. Safe as singleton.
    generate(text, language) → MP3 bytes
    """

    def generate(
        self,
        text: str,
        language: str = "Hindi",
        should_stop: Callable[[], bool] | None = None,
    ) -> bytes:
        """
        Convert text to MP3 bytes.

        Parameters
        ----------
        text     : AI response text (may contain markdown)
        language : detected language name (e.g. "Hindi", "Tamil")

        Returns
        -------
        bytes — MP3 audio data
        """
        clean_text = _clean(text)
        if not clean_text:
            raise ValueError("No speakable text after cleaning.")

        should_stop = should_stop or (lambda: False)
        lang_code   = _gtts_lang(language)
        chunks      = _split_sentences(clean_text)

        log.debug("TTS: lang=%s chunks=%d total_chars=%d", lang_code, len(chunks), len(clean_text))

        buf = io.BytesIO()
        for chunk in chunks:
            if should_stop():
                raise RuntimeError("TTS cancelled during generation.")

            try:
                tts = gTTS(text=chunk, lang=lang_code, slow=False)
                tts.write_to_fp(buf)
            except Exception as exc:
                if should_stop():
                    raise RuntimeError("TTS cancelled during generation.") from exc

                log.warning("TTS chunk failed (lang=%s): %s; retrying with 'hi'", lang_code, exc)
                # Fallback: retry with Hindi if the language code fails
                tts = gTTS(text=chunk, lang="hi", slow=False)
                tts.write_to_fp(buf)

            if should_stop():
                raise RuntimeError("TTS cancelled during generation.")

        buf.seek(0)
        return buf.read()
